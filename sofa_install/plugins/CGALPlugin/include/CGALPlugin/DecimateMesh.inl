/******************************************************************************
*                 SOFA, Simulation Open-Framework Architecture                *
*                    (c) 2006 INRIA, USTL, UJF, CNRS, MGH                     *
*                                                                             *
* This program is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU Lesser General Public License as published by    *
* the Free Software Foundation; either version 2.1 of the License, or (at     *
* your option) any later version.                                             *
*                                                                             *
* This program is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License *
* for more details.                                                           *
*                                                                             *
* You should have received a copy of the GNU Lesser General Public License    *
* along with this program. If not, see <http://www.gnu.org/licenses/>.        *
*******************************************************************************
* Authors: The SOFA Team and external contributors (see Authors.txt)          *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/
#pragma once

#include <CGALPlugin/DecimateMesh.h>

#include <iostream>
#include <fstream>

#include <sofa/simulation/AnimateBeginEvent.h>
#include <sofa/simulation/AnimateEndEvent.h>
#include <sofa/core/objectmodel/KeypressedEvent.h>
#include <sofa/core/objectmodel/KeyreleasedEvent.h>

using namespace sofa::core::objectmodel;

namespace cgal
{

template <class DataTypes>
DecimateMesh<DataTypes>::DecimateMesh()
    : d_inVertices(initData (&d_inVertices, "inputVertices", "List of vertices"))
    , d_inTriangles(initData(&d_inTriangles, "inputTriangles", "List of triangles"))
    , d_edgesTarget(initData(&d_edgesTarget, "targetedNumberOfEdges", "Desired number of edges after simplification"))
    , d_edgesRatio(initData(&d_edgesRatio, "targetedRatioOfEdges", "Ratio between the number of edges and number of initial edges"))
    , d_outVertices(initData (&d_outVertices, "outputPoints", "New vertices after decimation") )
    , d_outTriangles(initData (&d_outTriangles, "outputTriangles", "New triangles after decimation") )
    , d_outNormals(initData (&d_outNormals, "outputNormals", "New normals after decimation") )
    , d_writeToFile(initData (&d_writeToFile, false, "writeToFile", "Writes the decimated mesh into a file") )
{
}

template <class DataTypes>
DecimateMesh<DataTypes>::~DecimateMesh()
{
}

template <class DataTypes>
void DecimateMesh<DataTypes>::init()
{
    //Input
    addInput(&d_inVertices);
    addInput(&d_inTriangles);

    //Output
    addOutput(&d_outVertices);
    addOutput(&d_outTriangles);
    addOutput(&d_outNormals);

    setDirtyValue();

    reinit();
}

template <class DataTypes>
void DecimateMesh<DataTypes>::reinit()
{
    update();
}

template <class DataTypes>
void DecimateMesh<DataTypes>::doUpdate()
{
    // Writes topology into CGAL containers
    Surface surface;
    geometry_to_surface(surface);

    // Edge collapse simplification method

    msg_info() << "Initial mesh has " << d_inVertices.getValue().size() << " vertices and " << d_inTriangles.getValue().size() << " triangles." << msgendl
               << "Processing mesh simplification...";

    if (d_edgesTarget.getValue() != 0)
    {
        SMS::Count_stop_predicate<Surface> stop(d_edgesTarget.getValue());
#if CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,5,0)
        SMS::edge_collapse(surface
                           ,stop
                   #if CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,7,-1)
                           ,CGAL::parameters::vertex_index_map( get(CGAL::vertex_external_index,surface))
                   #else
                           , CGAL::vertex_index_map(get(CGAL::vertex_external_index, surface))
                   #endif // CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,7,0)
                           .halfedge_index_map( get(CGAL::halfedge_external_index,surface  )));
#else 
        SMS::edge_collapse(surface, stop, CGAL::vertex_index_map( boost::get(CGAL::vertex_external_index,surface)).edge_index_map( boost::get(CGAL::edge_external_index,surface  )));
#endif // CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,5,0)

    }
    else if (d_edgesRatio.getValue() != 0)
    {
        SMS::Count_ratio_stop_predicate<Surface> stop(d_edgesRatio.getValue());
#if CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,5,0)
        SMS::edge_collapse(surface
                           ,stop
                   #if CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,7,-1)
                           ,CGAL::parameters::vertex_index_map( get(CGAL::vertex_external_index,surface))
                   #else
                           , CGAL::vertex_index_map(get(CGAL::vertex_external_index, surface))
                   #endif // CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,7,0)
                           .halfedge_index_map( get(CGAL::halfedge_external_index,surface  )));
#else
        SMS::edge_collapse(surface, stop, CGAL::vertex_index_map( boost::get(CGAL::vertex_external_index,surface)).edge_index_map( boost::get(CGAL::edge_external_index,surface  )));
#endif // CGAL_VERSION_NR >= CGAL_VERSION_NUMBER(4,5,0)

    }
    else
    {
        msg_error() << "You must add a stop condition using either targetedNumberOfEdges or targetedRatioOfEdges" ;
    }


    // Writes results from CGAL to SOFA
    surface_to_geometry(surface);

    // Computes normals
    computeNormals();

    // Writes into file if necessary
    if (d_writeToFile.getValue())
    {
        writeObj();
    }

    msg_info() << "DecimateMesh: Decimated mesh has " << d_outVertices.getValue().size() << " vertices and " << d_outTriangles.getValue().size() << " triangles.";
}

template <class DataTypes>
void DecimateMesh<DataTypes>::writeObj()
{
    helper::ReadAccessor< Data< VecCoord > > outVertices = d_outVertices;
    helper::ReadAccessor< Data< SeqTriangles > > outTriangles = d_outTriangles;

    // Writes in Gmsh format
    std::ofstream myfile;
    myfile.open ("decimatedMesh.obj");
    for (unsigned int vertex=0; vertex<outVertices.size(); vertex++)
    {
        myfile << "v " << outVertices[vertex] << "\n";
    }
    for (unsigned int element=0; element<outTriangles.size(); element++)
    {
        myfile << "f " << outTriangles[element][0]+1 << " " << outTriangles[element][1]+1 << " " << outTriangles[element][2]+1 << "\n";
    }
    myfile.close();

    std::cout << "Decimated mesh written in decimatedMesh.obj" << std::endl;

}

template <class DataTypes>
void DecimateMesh<DataTypes>::computeNormals()
{
    helper::ReadAccessor< Data< VecCoord > > outVertices = d_outVertices;
    helper::ReadAccessor< Data< SeqTriangles > > outTriangles = d_outTriangles;

    helper::WriteAccessor< Data< type::vector<Vec3> > > outNormals = d_outNormals;


    for (unsigned int i=0; i<outVertices.size(); i++)
    {
        outNormals.push_back(Vec3(0, 0, 0));
    }

    for (unsigned int t=0; t<outTriangles.size(); t++)
    {
        Vec3 a = outVertices[ outTriangles[t][0] ];
        Vec3 b = outVertices[ outTriangles[t][1] ];
        Vec3 c = outVertices[ outTriangles[t][2] ];

        Vec3 z = cross(b-a, c-a);
        z.normalize();

        outNormals[ outTriangles[t][0] ] += z;
        outNormals[ outTriangles[t][1] ] += z;
        outNormals[ outTriangles[t][2] ] += z;
    }

    for (unsigned int i=0; i<outNormals.size(); i++)
    {
        outNormals[i].normalize();
    }
}

template <class DataTypes>
void DecimateMesh<DataTypes>::handleEvent(sofa::core::objectmodel::Event * /*event*/)
{
    //        std::cout << "handleEvent called" << std::endl;

    //        if (sofa::core::objectmodel::KeypressedEvent* ev = dynamic_cast<sofa::core::objectmodel::KeypressedEvent*>(event))
    //        {
    //            std::cout << "KeypressedEvent detected" << std::endl;
    //
    //            switch(ev->getKey())
    //            {
    //
    //            case 'M':
    //            case 'm':
    //                std::cout << "key pressed" << std::endl;
    //                writeObj();
    //                break;
    //            }
    //        }
}

template <class DataTypes>
void DecimateMesh<DataTypes>::geometry_to_surface(Surface &s)
{
    //        helper::ReadAccessor< Data< VecCoord > > inVertices = m_inVertices;
    //        helper::ReadAccessor< Data< SeqTriangles > > inTriangles = m_inTriangles;

    VecCoord inVertices = d_inVertices.getValue();
    SeqTriangles inTriangles = d_inTriangles.getValue();

    typedef Surface::HalfedgeDS HalfedgeDS;
    typedef geometry_to_surface_op<DataTypes, HalfedgeDS> GTSO;

    GTSO gen(inVertices, inTriangles);
    s.delegate(gen);
}

template <class DataTypes>
void DecimateMesh<DataTypes>::surface_to_geometry(Surface &s)
{
    helper::WriteAccessor< Data< VecCoord > > outVertices = d_outVertices;
    helper::WriteAccessor< Data< SeqTriangles > > outTriangles = d_outTriangles;

    for ( Surface::Facet_iterator fit( s.facets_begin() ), fend( s.facets_end() ); fit != fend; ++fit )
    {
        if ( fit->is_triangle() )
        {
            int indices[3];
            int tick = 0;

            Surface::Halfedge_around_facet_circulator hit( fit->facet_begin() ), hend( hit );
            do
            {
                Point p = hit->vertex()->point();

                if ( tick < 3 )
                {
                    bool toBeAdded = testVertexAndFindIndex(Vec3(p.x(), p.y(), p.z()), indices[tick++]);
                    if (!toBeAdded)
                    {
                        outVertices.push_back(Coord(p.x(), p.y(), p.z()));
                    }
                }
                else
                {
                    msg_error() << "We've got facets with more than 3 vertices even though the facet reported to be trianglular...";
                }

            }
            while( ++hit != hend );

            outTriangles.push_back( Triangle(indices[0], indices[1], indices[2]) );
        }
        else
        {
            msg_error() << "Skipping non-trianglular facet";
        }

    }
}

// --------------------------------------------------------------------------------------
// Tests if a vertex is already in the list and returns its index if it was
// Returns true if the vertex is in the list and false if it needs to be added
// --------------------------------------------------------------------------------------
template <class DataTypes>
bool DecimateMesh<DataTypes>::testVertexAndFindIndex(const Vec3 &vertex, int &index)
{
    VecCoord outVertices = d_outVertices.getValue();
    Vec3 outVertex;

    bool alreadyHere = false;

    for (unsigned int v=0; v< outVertices.size(); v++)
    {
        outVertex = Vec3(outVertices[v][0], outVertices[v][1], outVertices[v][2]);
        if ( (outVertex-vertex).norm() < 0.0000001)
        {
            alreadyHere = true;
            index = v;
        }
    }
    if (alreadyHere == false)
    {
        index = (int)outVertices.size();
    }

    return alreadyHere;
}


} //cgal
