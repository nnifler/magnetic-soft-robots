/********************************************************************************
** Form generated from reading UI file 'VisitorGUI.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_VISITORGUI_H
#define UI_VISITORGUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_VisitorGUI
{
public:
    QVBoxLayout *vboxLayout;
    QSplitter *splitterWindow;
    QWidget *traceWidget;
    QVBoxLayout *vboxLayout1;
    QSplitter *splitterStats;
    QTreeWidget *graphView;

    void setupUi(QWidget *VisitorGUI)
    {
        if (VisitorGUI->objectName().isEmpty())
            VisitorGUI->setObjectName(QString::fromUtf8("VisitorGUI"));
        VisitorGUI->resize(1000, 550);
        vboxLayout = new QVBoxLayout(VisitorGUI);
        vboxLayout->setSpacing(6);
        vboxLayout->setContentsMargins(11, 11, 11, 11);
        vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
        splitterWindow = new QSplitter(VisitorGUI);
        splitterWindow->setObjectName(QString::fromUtf8("splitterWindow"));
        splitterWindow->setOrientation(Qt::Vertical);
        traceWidget = new QWidget(splitterWindow);
        traceWidget->setObjectName(QString::fromUtf8("traceWidget"));
        vboxLayout1 = new QVBoxLayout(traceWidget);
        vboxLayout1->setSpacing(6);
        vboxLayout1->setContentsMargins(11, 11, 11, 11);
        vboxLayout1->setObjectName(QString::fromUtf8("vboxLayout1"));
        vboxLayout1->setContentsMargins(0, 0, 0, 0);
        splitterStats = new QSplitter(traceWidget);
        splitterStats->setObjectName(QString::fromUtf8("splitterStats"));
        splitterStats->setOrientation(Qt::Horizontal);
        graphView = new QTreeWidget(splitterStats);
        graphView->setObjectName(QString::fromUtf8("graphView"));
        splitterStats->addWidget(graphView);

        vboxLayout1->addWidget(splitterStats);

        splitterWindow->addWidget(traceWidget);

        vboxLayout->addWidget(splitterWindow);


        retranslateUi(VisitorGUI);

        QMetaObject::connectSlotsByName(VisitorGUI);
    } // setupUi

    void retranslateUi(QWidget *VisitorGUI)
    {
        VisitorGUI->setWindowTitle(QApplication::translate("VisitorGUI", "VisitorGUI", nullptr));
        QTreeWidgetItem *___qtreewidgetitem = graphView->headerItem();
        ___qtreewidgetitem->setText(3, QApplication::translate("VisitorGUI", "Value", nullptr));
        ___qtreewidgetitem->setText(2, QApplication::translate("VisitorGUI", "Type", nullptr));
        ___qtreewidgetitem->setText(1, QApplication::translate("VisitorGUI", "Time", nullptr));
        ___qtreewidgetitem->setText(0, QApplication::translate("VisitorGUI", "Graph", nullptr));
    } // retranslateUi

};

namespace Ui {
    class VisitorGUI: public Ui_VisitorGUI {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_VISITORGUI_H
