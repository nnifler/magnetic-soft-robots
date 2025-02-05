/********************************************************************************
** Form generated from reading UI file 'PluginManager.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PLUGINMANAGER_H
#define UI_PLUGINMANAGER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_PluginManager
{
public:
    QGridLayout *gridLayout;
    QVBoxLayout *vboxLayout;
    QSplitter *unnamed;
    QTreeWidget *listPlugins;
    QWidget *layout24;
    QHBoxLayout *hboxLayout;
    QVBoxLayout *vboxLayout1;
    QLabel *description_label;
    QTextEdit *description;
    QTreeWidget *listComponents;
    QHBoxLayout *hboxLayout1;
    QPushButton *buttonAdd;
    QPushButton *buttonRemove;
    QSpacerItem *Horizontal_Spacing2;
    QPushButton *buttonClose;

    void setupUi(QDialog *PluginManager)
    {
        if (PluginManager->objectName().isEmpty())
            PluginManager->setObjectName(QString::fromUtf8("PluginManager"));
        PluginManager->setEnabled(true);
        PluginManager->resize(800, 400);
        PluginManager->setSizeGripEnabled(false);
        gridLayout = new QGridLayout(PluginManager);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        vboxLayout = new QVBoxLayout();
        vboxLayout->setSpacing(6);
        vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
        unnamed = new QSplitter(PluginManager);
        unnamed->setObjectName(QString::fromUtf8("unnamed"));
        unnamed->setOrientation(Qt::Vertical);
        listPlugins = new QTreeWidget(unnamed);
        QTreeWidgetItem *__qtreewidgetitem = new QTreeWidgetItem();
        __qtreewidgetitem->setText(0, QString::fromUtf8("1"));
        listPlugins->setHeaderItem(__qtreewidgetitem);
        listPlugins->setObjectName(QString::fromUtf8("listPlugins"));
        listPlugins->setMinimumSize(QSize(416, 0));
        listPlugins->setMidLineWidth(1);
        listPlugins->setAllColumnsShowFocus(true);
        listPlugins->setProperty("showSortIndicator", QVariant(true));
        listPlugins->setProperty("itemMargin", QVariant(4));
        unnamed->addWidget(listPlugins);
        layout24 = new QWidget(unnamed);
        layout24->setObjectName(QString::fromUtf8("layout24"));
        hboxLayout = new QHBoxLayout(layout24);
        hboxLayout->setSpacing(6);
        hboxLayout->setContentsMargins(11, 11, 11, 11);
        hboxLayout->setObjectName(QString::fromUtf8("hboxLayout"));
        hboxLayout->setContentsMargins(0, 0, 0, 0);
        vboxLayout1 = new QVBoxLayout();
        vboxLayout1->setSpacing(6);
        vboxLayout1->setObjectName(QString::fromUtf8("vboxLayout1"));
        description_label = new QLabel(layout24);
        description_label->setObjectName(QString::fromUtf8("description_label"));
        description_label->setWordWrap(false);

        vboxLayout1->addWidget(description_label);

        description = new QTextEdit(layout24);
        description->setObjectName(QString::fromUtf8("description"));
        description->setEnabled(true);
        description->setUndoRedoEnabled(false);
        description->setReadOnly(true);

        vboxLayout1->addWidget(description);


        hboxLayout->addLayout(vboxLayout1);

        listComponents = new QTreeWidget(layout24);
        QTreeWidgetItem *__qtreewidgetitem1 = new QTreeWidgetItem();
        __qtreewidgetitem1->setText(0, QString::fromUtf8("1"));
        listComponents->setHeaderItem(__qtreewidgetitem1);
        listComponents->setObjectName(QString::fromUtf8("listComponents"));
        listComponents->setEnabled(true);

        hboxLayout->addWidget(listComponents);

        unnamed->addWidget(layout24);

        vboxLayout->addWidget(unnamed);


        gridLayout->addLayout(vboxLayout, 0, 0, 1, 1);

        hboxLayout1 = new QHBoxLayout();
        hboxLayout1->setSpacing(6);
        hboxLayout1->setObjectName(QString::fromUtf8("hboxLayout1"));
        buttonAdd = new QPushButton(PluginManager);
        buttonAdd->setObjectName(QString::fromUtf8("buttonAdd"));
        buttonAdd->setAutoDefault(true);

        hboxLayout1->addWidget(buttonAdd);

        buttonRemove = new QPushButton(PluginManager);
        buttonRemove->setObjectName(QString::fromUtf8("buttonRemove"));
        buttonRemove->setAutoDefault(true);

        hboxLayout1->addWidget(buttonRemove);

        Horizontal_Spacing2 = new QSpacerItem(237, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout1->addItem(Horizontal_Spacing2);

        buttonClose = new QPushButton(PluginManager);
        buttonClose->setObjectName(QString::fromUtf8("buttonClose"));
        buttonClose->setAutoDefault(true);

        hboxLayout1->addWidget(buttonClose);


        gridLayout->addLayout(hboxLayout1, 1, 0, 1, 1);


        retranslateUi(PluginManager);
        QObject::connect(buttonClose, SIGNAL(clicked()), PluginManager, SLOT(close()));

        buttonAdd->setDefault(true);


        QMetaObject::connectSlotsByName(PluginManager);
    } // setupUi

    void retranslateUi(QDialog *PluginManager)
    {
        PluginManager->setWindowTitle(QApplication::translate("PluginManager", "Plugin Manager", nullptr));
        description_label->setText(QApplication::translate("PluginManager", "Description", nullptr));
        buttonAdd->setText(QApplication::translate("PluginManager", "&Add...", nullptr));
#ifndef QT_NO_SHORTCUT
        buttonAdd->setShortcut(QApplication::translate("PluginManager", "Alt+A", nullptr));
#endif // QT_NO_SHORTCUT
        buttonRemove->setText(QApplication::translate("PluginManager", "&Remove", nullptr));
#ifndef QT_NO_SHORTCUT
        buttonRemove->setShortcut(QApplication::translate("PluginManager", "Alt+R", nullptr));
#endif // QT_NO_SHORTCUT
        buttonClose->setText(QApplication::translate("PluginManager", "&Close", nullptr));
#ifndef QT_NO_SHORTCUT
        buttonClose->setShortcut(QApplication::translate("PluginManager", "Alt+C", nullptr));
#endif // QT_NO_SHORTCUT
    } // retranslateUi

};

namespace Ui {
    class PluginManager: public Ui_PluginManager {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PLUGINMANAGER_H
