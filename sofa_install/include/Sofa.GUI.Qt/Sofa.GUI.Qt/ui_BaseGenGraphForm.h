/********************************************************************************
** Form generated from reading UI file 'BaseGenGraphForm.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_BASEGENGRAPHFORM_H
#define UI_BASEGENGRAPHFORM_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_BaseGenGraphForm
{
public:
    QVBoxLayout *vboxLayout;
    QGridLayout *gridLayout;
    QLabel *filenameLabel;
    QPushButton *browseButton;
    QLineEdit *filename;
    QHBoxLayout *hboxLayout;
    QGroupBox *layoutGroup;
    QVBoxLayout *vboxLayout1;
    QRadioButton *layoutDirV;
    QRadioButton *layoutDirH;
    QRadioButton *layoutSpring;
    QRadioButton *layoutRadial;
    QGroupBox *outputsBox;
    QVBoxLayout *vboxLayout2;
    QCheckBox *genPNG;
    QCheckBox *genPS;
    QCheckBox *genFIG;
    QCheckBox *genSVG;
    QHBoxLayout *hboxLayout1;
    QLabel *presetLabel;
    QComboBox *presetFilter;
    QGroupBox *filterBox;
    QGridLayout *gridLayout1;
    QCheckBox *showSolvers;
    QCheckBox *showMechanicalStates;
    QCheckBox *showForceFields;
    QCheckBox *showInteractionForceFields;
    QCheckBox *showConstraints;
    QCheckBox *showMass;
    QCheckBox *showMechanicalMappings;
    QCheckBox *showTopology;
    QCheckBox *showMappings;
    QCheckBox *showCollisionModels;
    QCheckBox *showVisualModels;
    QCheckBox *showCollisionPipeline;
    QCheckBox *showBehaviorModels;
    QCheckBox *showContext;
    QCheckBox *showObjects;
    QCheckBox *showNodes;
    QHBoxLayout *hboxLayout2;
    QGroupBox *groupNodeLabel;
    QVBoxLayout *vboxLayout3;
    QCheckBox *labelNodeName;
    QCheckBox *labelNodeClass;
    QGroupBox *groupObjectLabel;
    QVBoxLayout *vboxLayout4;
    QCheckBox *labelObjectName;
    QCheckBox *labelObjectClass;
    QHBoxLayout *hboxLayout3;
    QSpacerItem *spacer1;
    QPushButton *displayButton;
    QPushButton *exportButton;
    QPushButton *closeButton;

    void setupUi(QDialog *BaseGenGraphForm)
    {
        if (BaseGenGraphForm->objectName().isEmpty())
            BaseGenGraphForm->setObjectName(QString::fromUtf8("BaseGenGraphForm"));
        BaseGenGraphForm->resize(382, 654);
        vboxLayout = new QVBoxLayout(BaseGenGraphForm);
        vboxLayout->setSpacing(6);
        vboxLayout->setContentsMargins(11, 11, 11, 11);
        vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
        gridLayout = new QGridLayout();
        gridLayout->setSpacing(6);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        filenameLabel = new QLabel(BaseGenGraphForm);
        filenameLabel->setObjectName(QString::fromUtf8("filenameLabel"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(1);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(filenameLabel->sizePolicy().hasHeightForWidth());
        filenameLabel->setSizePolicy(sizePolicy);
        filenameLabel->setWordWrap(false);

        gridLayout->addWidget(filenameLabel, 0, 0, 1, 1);

        browseButton = new QPushButton(BaseGenGraphForm);
        browseButton->setObjectName(QString::fromUtf8("browseButton"));

        gridLayout->addWidget(browseButton, 0, 1, 1, 1);

        filename = new QLineEdit(BaseGenGraphForm);
        filename->setObjectName(QString::fromUtf8("filename"));

        gridLayout->addWidget(filename, 1, 0, 1, 2);


        vboxLayout->addLayout(gridLayout);

        hboxLayout = new QHBoxLayout();
        hboxLayout->setSpacing(6);
        hboxLayout->setObjectName(QString::fromUtf8("hboxLayout"));
        layoutGroup = new QGroupBox(BaseGenGraphForm);
        layoutGroup->setObjectName(QString::fromUtf8("layoutGroup"));
        vboxLayout1 = new QVBoxLayout(layoutGroup);
        vboxLayout1->setSpacing(6);
        vboxLayout1->setContentsMargins(11, 11, 11, 11);
        vboxLayout1->setObjectName(QString::fromUtf8("vboxLayout1"));
        layoutDirV = new QRadioButton(layoutGroup);
        layoutDirV->setObjectName(QString::fromUtf8("layoutDirV"));
        layoutDirV->setChecked(true);

        vboxLayout1->addWidget(layoutDirV);

        layoutDirH = new QRadioButton(layoutGroup);
        layoutDirH->setObjectName(QString::fromUtf8("layoutDirH"));

        vboxLayout1->addWidget(layoutDirH);

        layoutSpring = new QRadioButton(layoutGroup);
        layoutSpring->setObjectName(QString::fromUtf8("layoutSpring"));

        vboxLayout1->addWidget(layoutSpring);

        layoutRadial = new QRadioButton(layoutGroup);
        layoutRadial->setObjectName(QString::fromUtf8("layoutRadial"));

        vboxLayout1->addWidget(layoutRadial);


        hboxLayout->addWidget(layoutGroup);

        outputsBox = new QGroupBox(BaseGenGraphForm);
        outputsBox->setObjectName(QString::fromUtf8("outputsBox"));
        vboxLayout2 = new QVBoxLayout(outputsBox);
        vboxLayout2->setSpacing(6);
        vboxLayout2->setContentsMargins(11, 11, 11, 11);
        vboxLayout2->setObjectName(QString::fromUtf8("vboxLayout2"));
        genPNG = new QCheckBox(outputsBox);
        genPNG->setObjectName(QString::fromUtf8("genPNG"));
        genPNG->setChecked(true);

        vboxLayout2->addWidget(genPNG);

        genPS = new QCheckBox(outputsBox);
        genPS->setObjectName(QString::fromUtf8("genPS"));

        vboxLayout2->addWidget(genPS);

        genFIG = new QCheckBox(outputsBox);
        genFIG->setObjectName(QString::fromUtf8("genFIG"));

        vboxLayout2->addWidget(genFIG);

        genSVG = new QCheckBox(outputsBox);
        genSVG->setObjectName(QString::fromUtf8("genSVG"));

        vboxLayout2->addWidget(genSVG);


        hboxLayout->addWidget(outputsBox);


        vboxLayout->addLayout(hboxLayout);

        hboxLayout1 = new QHBoxLayout();
        hboxLayout1->setSpacing(6);
        hboxLayout1->setObjectName(QString::fromUtf8("hboxLayout1"));
        presetLabel = new QLabel(BaseGenGraphForm);
        presetLabel->setObjectName(QString::fromUtf8("presetLabel"));
        presetLabel->setWordWrap(false);

        hboxLayout1->addWidget(presetLabel);

        presetFilter = new QComboBox(BaseGenGraphForm);
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->addItem(QString());
        presetFilter->setObjectName(QString::fromUtf8("presetFilter"));
        QSizePolicy sizePolicy1(QSizePolicy::Minimum, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(1);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(presetFilter->sizePolicy().hasHeightForWidth());
        presetFilter->setSizePolicy(sizePolicy1);
        presetFilter->setEditable(true);
        presetFilter->setInsertPolicy(QComboBox::InsertAtTop);
        presetFilter->setDuplicatesEnabled(false);
        presetFilter->setFrame(true);

        hboxLayout1->addWidget(presetFilter);


        vboxLayout->addLayout(hboxLayout1);

        filterBox = new QGroupBox(BaseGenGraphForm);
        filterBox->setObjectName(QString::fromUtf8("filterBox"));
        gridLayout1 = new QGridLayout(filterBox);
        gridLayout1->setSpacing(6);
        gridLayout1->setContentsMargins(11, 11, 11, 11);
        gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
        showSolvers = new QCheckBox(filterBox);
        showSolvers->setObjectName(QString::fromUtf8("showSolvers"));
        showSolvers->setChecked(true);

        gridLayout1->addWidget(showSolvers, 0, 1, 1, 1);

        showMechanicalStates = new QCheckBox(filterBox);
        showMechanicalStates->setObjectName(QString::fromUtf8("showMechanicalStates"));
        showMechanicalStates->setChecked(true);

        gridLayout1->addWidget(showMechanicalStates, 1, 1, 1, 1);

        showForceFields = new QCheckBox(filterBox);
        showForceFields->setObjectName(QString::fromUtf8("showForceFields"));
        showForceFields->setChecked(true);

        gridLayout1->addWidget(showForceFields, 2, 1, 1, 1);

        showInteractionForceFields = new QCheckBox(filterBox);
        showInteractionForceFields->setObjectName(QString::fromUtf8("showInteractionForceFields"));
        showInteractionForceFields->setChecked(true);

        gridLayout1->addWidget(showInteractionForceFields, 3, 1, 1, 1);

        showConstraints = new QCheckBox(filterBox);
        showConstraints->setObjectName(QString::fromUtf8("showConstraints"));
        showConstraints->setChecked(true);

        gridLayout1->addWidget(showConstraints, 4, 1, 1, 1);

        showMass = new QCheckBox(filterBox);
        showMass->setObjectName(QString::fromUtf8("showMass"));
        showMass->setChecked(true);

        gridLayout1->addWidget(showMass, 5, 1, 1, 1);

        showMechanicalMappings = new QCheckBox(filterBox);
        showMechanicalMappings->setObjectName(QString::fromUtf8("showMechanicalMappings"));
        showMechanicalMappings->setChecked(true);

        gridLayout1->addWidget(showMechanicalMappings, 7, 1, 1, 1);

        showTopology = new QCheckBox(filterBox);
        showTopology->setObjectName(QString::fromUtf8("showTopology"));
        showTopology->setChecked(true);

        gridLayout1->addWidget(showTopology, 6, 1, 1, 1);

        showMappings = new QCheckBox(filterBox);
        showMappings->setObjectName(QString::fromUtf8("showMappings"));
        showMappings->setChecked(true);

        gridLayout1->addWidget(showMappings, 5, 0, 1, 1);

        showCollisionModels = new QCheckBox(filterBox);
        showCollisionModels->setObjectName(QString::fromUtf8("showCollisionModels"));
        showCollisionModels->setChecked(true);

        gridLayout1->addWidget(showCollisionModels, 3, 0, 1, 1);

        showVisualModels = new QCheckBox(filterBox);
        showVisualModels->setObjectName(QString::fromUtf8("showVisualModels"));
        showVisualModels->setChecked(true);

        gridLayout1->addWidget(showVisualModels, 4, 0, 1, 1);

        showCollisionPipeline = new QCheckBox(filterBox);
        showCollisionPipeline->setObjectName(QString::fromUtf8("showCollisionPipeline"));
        showCollisionPipeline->setChecked(true);

        gridLayout1->addWidget(showCollisionPipeline, 7, 0, 1, 1);

        showBehaviorModels = new QCheckBox(filterBox);
        showBehaviorModels->setObjectName(QString::fromUtf8("showBehaviorModels"));
        showBehaviorModels->setChecked(true);

        gridLayout1->addWidget(showBehaviorModels, 2, 0, 1, 1);

        showContext = new QCheckBox(filterBox);
        showContext->setObjectName(QString::fromUtf8("showContext"));
        showContext->setChecked(true);

        gridLayout1->addWidget(showContext, 6, 0, 1, 1);

        showObjects = new QCheckBox(filterBox);
        showObjects->setObjectName(QString::fromUtf8("showObjects"));
        showObjects->setChecked(true);

        gridLayout1->addWidget(showObjects, 1, 0, 1, 1);

        showNodes = new QCheckBox(filterBox);
        showNodes->setObjectName(QString::fromUtf8("showNodes"));
        showNodes->setChecked(true);

        gridLayout1->addWidget(showNodes, 0, 0, 1, 1);


        vboxLayout->addWidget(filterBox);

        hboxLayout2 = new QHBoxLayout();
        hboxLayout2->setSpacing(6);
        hboxLayout2->setObjectName(QString::fromUtf8("hboxLayout2"));
        groupNodeLabel = new QGroupBox(BaseGenGraphForm);
        groupNodeLabel->setObjectName(QString::fromUtf8("groupNodeLabel"));
        vboxLayout3 = new QVBoxLayout(groupNodeLabel);
        vboxLayout3->setSpacing(6);
        vboxLayout3->setContentsMargins(11, 11, 11, 11);
        vboxLayout3->setObjectName(QString::fromUtf8("vboxLayout3"));
        labelNodeName = new QCheckBox(groupNodeLabel);
        labelNodeName->setObjectName(QString::fromUtf8("labelNodeName"));
        labelNodeName->setChecked(true);

        vboxLayout3->addWidget(labelNodeName);

        labelNodeClass = new QCheckBox(groupNodeLabel);
        labelNodeClass->setObjectName(QString::fromUtf8("labelNodeClass"));

        vboxLayout3->addWidget(labelNodeClass);


        hboxLayout2->addWidget(groupNodeLabel);

        groupObjectLabel = new QGroupBox(BaseGenGraphForm);
        groupObjectLabel->setObjectName(QString::fromUtf8("groupObjectLabel"));
        vboxLayout4 = new QVBoxLayout(groupObjectLabel);
        vboxLayout4->setSpacing(6);
        vboxLayout4->setContentsMargins(11, 11, 11, 11);
        vboxLayout4->setObjectName(QString::fromUtf8("vboxLayout4"));
        labelObjectName = new QCheckBox(groupObjectLabel);
        labelObjectName->setObjectName(QString::fromUtf8("labelObjectName"));
        labelObjectName->setChecked(true);

        vboxLayout4->addWidget(labelObjectName);

        labelObjectClass = new QCheckBox(groupObjectLabel);
        labelObjectClass->setObjectName(QString::fromUtf8("labelObjectClass"));
        labelObjectClass->setChecked(true);

        vboxLayout4->addWidget(labelObjectClass);


        hboxLayout2->addWidget(groupObjectLabel);


        vboxLayout->addLayout(hboxLayout2);

        hboxLayout3 = new QHBoxLayout();
        hboxLayout3->setSpacing(6);
        hboxLayout3->setObjectName(QString::fromUtf8("hboxLayout3"));
        spacer1 = new QSpacerItem(16, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout3->addItem(spacer1);

        displayButton = new QPushButton(BaseGenGraphForm);
        displayButton->setObjectName(QString::fromUtf8("displayButton"));
        displayButton->setEnabled(false);

        hboxLayout3->addWidget(displayButton);

        exportButton = new QPushButton(BaseGenGraphForm);
        exportButton->setObjectName(QString::fromUtf8("exportButton"));

        hboxLayout3->addWidget(exportButton);

        closeButton = new QPushButton(BaseGenGraphForm);
        closeButton->setObjectName(QString::fromUtf8("closeButton"));

        hboxLayout3->addWidget(closeButton);


        vboxLayout->addLayout(hboxLayout3);

#ifndef QT_NO_SHORTCUT
        filenameLabel->setBuddy(filename);
#endif // QT_NO_SHORTCUT
        QWidget::setTabOrder(filename, browseButton);
        QWidget::setTabOrder(browseButton, layoutDirV);
        QWidget::setTabOrder(layoutDirV, layoutDirH);
        QWidget::setTabOrder(layoutDirH, layoutSpring);
        QWidget::setTabOrder(layoutSpring, layoutRadial);
        QWidget::setTabOrder(layoutRadial, genPNG);
        QWidget::setTabOrder(genPNG, genPS);
        QWidget::setTabOrder(genPS, genFIG);
        QWidget::setTabOrder(genFIG, genSVG);
        QWidget::setTabOrder(genSVG, showSolvers);
        QWidget::setTabOrder(showSolvers, showMechanicalStates);
        QWidget::setTabOrder(showMechanicalStates, showForceFields);
        QWidget::setTabOrder(showForceFields, showInteractionForceFields);
        QWidget::setTabOrder(showInteractionForceFields, showConstraints);
        QWidget::setTabOrder(showConstraints, showMass);
        QWidget::setTabOrder(showMass, showMechanicalMappings);
        QWidget::setTabOrder(showMechanicalMappings, showTopology);
        QWidget::setTabOrder(showTopology, showMappings);
        QWidget::setTabOrder(showMappings, showCollisionModels);
        QWidget::setTabOrder(showCollisionModels, showVisualModels);
        QWidget::setTabOrder(showVisualModels, showCollisionPipeline);
        QWidget::setTabOrder(showCollisionPipeline, showBehaviorModels);
        QWidget::setTabOrder(showBehaviorModels, showContext);
        QWidget::setTabOrder(showContext, showObjects);
        QWidget::setTabOrder(showObjects, showNodes);
        QWidget::setTabOrder(showNodes, labelNodeName);
        QWidget::setTabOrder(labelNodeName, labelNodeClass);
        QWidget::setTabOrder(labelNodeClass, labelObjectName);
        QWidget::setTabOrder(labelObjectName, labelObjectClass);
        QWidget::setTabOrder(labelObjectClass, displayButton);
        QWidget::setTabOrder(displayButton, exportButton);

        retranslateUi(BaseGenGraphForm);
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showBehaviorModels, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showCollisionModels, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showVisualModels, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showMappings, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showContext, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showCollisionPipeline, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showSolvers, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showMechanicalStates, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showForceFields, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showInteractionForceFields, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showConstraints, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showMass, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showTopology, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), showMechanicalMappings, SLOT(setEnabled(bool)));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), groupObjectLabel, SLOT(setEnabled(bool)));
        QObject::connect(showNodes, SIGNAL(toggled(bool)), groupNodeLabel, SLOT(setEnabled(bool)));
        QObject::connect(showNodes, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showObjects, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showBehaviorModels, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showCollisionModels, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showVisualModels, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showMappings, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showContext, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showCollisionPipeline, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showSolvers, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showMechanicalStates, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showForceFields, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showInteractionForceFields, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showConstraints, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showMass, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showTopology, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));
        QObject::connect(showMechanicalMappings, SIGNAL(toggled(bool)), presetFilter, SLOT(clearEditText()));

        exportButton->setDefault(true);


        QMetaObject::connectSlotsByName(BaseGenGraphForm);
    } // setupUi

    void retranslateUi(QDialog *BaseGenGraphForm)
    {
        BaseGenGraphForm->setWindowTitle(QApplication::translate("BaseGenGraphForm", "Sofa Graph Export", nullptr));
        filenameLabel->setText(QApplication::translate("BaseGenGraphForm", "Output DOT &File", nullptr));
        browseButton->setText(QApplication::translate("BaseGenGraphForm", "Browse...", nullptr));
        filename->setText(QApplication::translate("BaseGenGraphForm", "untitled", nullptr));
        layoutGroup->setTitle(QApplication::translate("BaseGenGraphForm", "Layout", nullptr));
        layoutDirV->setText(QApplication::translate("BaseGenGraphForm", "Directed Vertically", nullptr));
        layoutDirH->setText(QApplication::translate("BaseGenGraphForm", "Directed Horizontally", nullptr));
        layoutSpring->setText(QApplication::translate("BaseGenGraphForm", "Undirected Spring", nullptr));
        layoutRadial->setText(QApplication::translate("BaseGenGraphForm", "Undirected Radial", nullptr));
        outputsBox->setTitle(QApplication::translate("BaseGenGraphForm", "Outputs", nullptr));
        genPNG->setText(QApplication::translate("BaseGenGraphForm", "Generate PNG", nullptr));
        genPS->setText(QApplication::translate("BaseGenGraphForm", "Generate PS", nullptr));
        genFIG->setText(QApplication::translate("BaseGenGraphForm", "Generate FIG", nullptr));
        genSVG->setText(QApplication::translate("BaseGenGraphForm", "Generate SVG", nullptr));
        presetLabel->setText(QApplication::translate("BaseGenGraphForm", "Presets", nullptr));
        presetFilter->setItemText(0, QApplication::translate("BaseGenGraphForm", "Full Graph", nullptr));
        presetFilter->setItemText(1, QApplication::translate("BaseGenGraphForm", "All Objects", nullptr));
        presetFilter->setItemText(2, QApplication::translate("BaseGenGraphForm", "All Nodes", nullptr));
        presetFilter->setItemText(3, QApplication::translate("BaseGenGraphForm", "Mechanical Graph", nullptr));
        presetFilter->setItemText(4, QApplication::translate("BaseGenGraphForm", "Mechanical Objects", nullptr));
        presetFilter->setItemText(5, QApplication::translate("BaseGenGraphForm", "Visual Graph", nullptr));
        presetFilter->setItemText(6, QApplication::translate("BaseGenGraphForm", "Visual Objects", nullptr));
        presetFilter->setItemText(7, QApplication::translate("BaseGenGraphForm", "Collision Graph", nullptr));
        presetFilter->setItemText(8, QApplication::translate("BaseGenGraphForm", "Collision Objects", nullptr));
        presetFilter->setItemText(9, QApplication::translate("BaseGenGraphForm", "Collision Response Graph", nullptr));
        presetFilter->setItemText(10, QApplication::translate("BaseGenGraphForm", "Collision Response Objects", nullptr));

        filterBox->setTitle(QApplication::translate("BaseGenGraphForm", "Filter", nullptr));
        showSolvers->setText(QApplication::translate("BaseGenGraphForm", "Solvers", nullptr));
        showMechanicalStates->setText(QApplication::translate("BaseGenGraphForm", "Mechanical Models", nullptr));
        showForceFields->setText(QApplication::translate("BaseGenGraphForm", "Force Fields", nullptr));
        showInteractionForceFields->setText(QApplication::translate("BaseGenGraphForm", "Interaction Force Fields", nullptr));
        showConstraints->setText(QApplication::translate("BaseGenGraphForm", "Constraints", nullptr));
        showMass->setText(QApplication::translate("BaseGenGraphForm", "Mass", nullptr));
        showMechanicalMappings->setText(QApplication::translate("BaseGenGraphForm", "Mechanical Mappings", nullptr));
        showTopology->setText(QApplication::translate("BaseGenGraphForm", "Topology", nullptr));
        showMappings->setText(QApplication::translate("BaseGenGraphForm", "Mappings", nullptr));
        showCollisionModels->setText(QApplication::translate("BaseGenGraphForm", "Collision Models", nullptr));
        showVisualModels->setText(QApplication::translate("BaseGenGraphForm", "Visual Models", nullptr));
        showCollisionPipeline->setText(QApplication::translate("BaseGenGraphForm", "Collision Pipeline", nullptr));
        showBehaviorModels->setText(QApplication::translate("BaseGenGraphForm", "Behavior Models", nullptr));
        showContext->setText(QApplication::translate("BaseGenGraphForm", "Context", nullptr));
        showObjects->setText(QApplication::translate("BaseGenGraphForm", "Objects", nullptr));
        showNodes->setText(QApplication::translate("BaseGenGraphForm", "Nodes", nullptr));
        groupNodeLabel->setTitle(QApplication::translate("BaseGenGraphForm", "Nodes Labels", nullptr));
        labelNodeName->setText(QApplication::translate("BaseGenGraphForm", "Name", nullptr));
        labelNodeClass->setText(QApplication::translate("BaseGenGraphForm", "Class", nullptr));
        groupObjectLabel->setTitle(QApplication::translate("BaseGenGraphForm", "Objects Labels", nullptr));
        labelObjectName->setText(QApplication::translate("BaseGenGraphForm", "Name", nullptr));
        labelObjectClass->setText(QApplication::translate("BaseGenGraphForm", "Class", nullptr));
        displayButton->setText(QApplication::translate("BaseGenGraphForm", "&Display", nullptr));
#ifndef QT_NO_SHORTCUT
        displayButton->setShortcut(QApplication::translate("BaseGenGraphForm", "Alt+D", nullptr));
#endif // QT_NO_SHORTCUT
        exportButton->setText(QApplication::translate("BaseGenGraphForm", "&Export", nullptr));
#ifndef QT_NO_SHORTCUT
        exportButton->setShortcut(QApplication::translate("BaseGenGraphForm", "Alt+E", nullptr));
#endif // QT_NO_SHORTCUT
        closeButton->setText(QApplication::translate("BaseGenGraphForm", "&Close", nullptr));
#ifndef QT_NO_SHORTCUT
        closeButton->setShortcut(QApplication::translate("BaseGenGraphForm", "Alt+C", nullptr));
#endif // QT_NO_SHORTCUT
    } // retranslateUi

};

namespace Ui {
    class BaseGenGraphForm: public Ui_BaseGenGraphForm {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_BASEGENGRAPHFORM_H
