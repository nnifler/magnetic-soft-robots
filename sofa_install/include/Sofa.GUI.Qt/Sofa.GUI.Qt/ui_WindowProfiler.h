/********************************************************************************
** Form generated from reading UI file 'WindowProfiler.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_WINDOWPROFILER_H
#define UI_WINDOWPROFILER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollBar>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_WindowProfiler
{
public:
    QGridLayout *gridLayout;
    QVBoxLayout *main_layout;
    QHBoxLayout *Layout_graph;
    QSpacerItem *verticalSpacer_2;
    QHBoxLayout *LayoutBottom;
    QVBoxLayout *Layout_summary;
    QLabel *label_summary;
    QGridLayout *Layout_summaryInfo;
    QLabel *label_stepN;
    QLabel *label_overhead;
    QLabel *label_stepValue;
    QLabel *label_time;
    QLabel *label_timeValue;
    QLabel *label_overheadValue;
    QLabel *label_timersCounter;
    QLabel *label_timersCounterValue;
    QScrollBar *step_scroller;
    QSpacerItem *verticalSpacer;
    QVBoxLayout *Layout_tree;
    QHBoxLayout *horizontalLayout;
    QSpacerItem *horizontalSpacer;
    QPushButton *CollapseAllButton;
    QPushButton *ExpandAllButton;
    QTreeWidget *tree_steps;

    void setupUi(QWidget *WindowProfiler)
    {
        if (WindowProfiler->objectName().isEmpty())
            WindowProfiler->setObjectName(QString::fromUtf8("WindowProfiler"));
        WindowProfiler->setEnabled(true);
        WindowProfiler->resize(950, 760);
        WindowProfiler->setProperty("sizeGripEnabled", QVariant(false));
        gridLayout = new QGridLayout(WindowProfiler);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        main_layout = new QVBoxLayout();
        main_layout->setSpacing(6);
        main_layout->setObjectName(QString::fromUtf8("main_layout"));
        Layout_graph = new QHBoxLayout();
        Layout_graph->setSpacing(6);
        Layout_graph->setObjectName(QString::fromUtf8("Layout_graph"));
        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        Layout_graph->addItem(verticalSpacer_2);


        main_layout->addLayout(Layout_graph);

        LayoutBottom = new QHBoxLayout();
        LayoutBottom->setSpacing(6);
        LayoutBottom->setObjectName(QString::fromUtf8("LayoutBottom"));
        Layout_summary = new QVBoxLayout();
        Layout_summary->setSpacing(6);
        Layout_summary->setObjectName(QString::fromUtf8("Layout_summary"));
        Layout_summary->setSizeConstraint(QLayout::SetFixedSize);
        label_summary = new QLabel(WindowProfiler);
        label_summary->setObjectName(QString::fromUtf8("label_summary"));
        QFont font;
        font.setBold(true);
        font.setUnderline(true);
        font.setWeight(75);
        label_summary->setFont(font);

        Layout_summary->addWidget(label_summary);

        Layout_summaryInfo = new QGridLayout();
        Layout_summaryInfo->setSpacing(6);
        Layout_summaryInfo->setObjectName(QString::fromUtf8("Layout_summaryInfo"));
        label_stepN = new QLabel(WindowProfiler);
        label_stepN->setObjectName(QString::fromUtf8("label_stepN"));

        Layout_summaryInfo->addWidget(label_stepN, 0, 0, 1, 1);

        label_overhead = new QLabel(WindowProfiler);
        label_overhead->setObjectName(QString::fromUtf8("label_overhead"));

        Layout_summaryInfo->addWidget(label_overhead, 2, 0, 1, 1);

        label_stepValue = new QLabel(WindowProfiler);
        label_stepValue->setObjectName(QString::fromUtf8("label_stepValue"));

        Layout_summaryInfo->addWidget(label_stepValue, 0, 1, 1, 1);

        label_time = new QLabel(WindowProfiler);
        label_time->setObjectName(QString::fromUtf8("label_time"));

        Layout_summaryInfo->addWidget(label_time, 1, 0, 1, 1);

        label_timeValue = new QLabel(WindowProfiler);
        label_timeValue->setObjectName(QString::fromUtf8("label_timeValue"));

        Layout_summaryInfo->addWidget(label_timeValue, 1, 1, 1, 1);

        label_overheadValue = new QLabel(WindowProfiler);
        label_overheadValue->setObjectName(QString::fromUtf8("label_overheadValue"));

        Layout_summaryInfo->addWidget(label_overheadValue, 2, 1, 1, 1);

        label_timersCounter = new QLabel(WindowProfiler);
        label_timersCounter->setObjectName(QString::fromUtf8("label_timersCounter"));

        Layout_summaryInfo->addWidget(label_timersCounter, 3, 0, 1, 1);

        label_timersCounterValue = new QLabel(WindowProfiler);
        label_timersCounterValue->setObjectName(QString::fromUtf8("label_timersCounterValue"));

        Layout_summaryInfo->addWidget(label_timersCounterValue, 3, 1, 1, 1);


        Layout_summary->addLayout(Layout_summaryInfo);

        step_scroller = new QScrollBar(WindowProfiler);
        step_scroller->setObjectName(QString::fromUtf8("step_scroller"));
        step_scroller->setOrientation(Qt::Horizontal);

        Layout_summary->addWidget(step_scroller);

        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        Layout_summary->addItem(verticalSpacer);


        LayoutBottom->addLayout(Layout_summary);

        Layout_tree = new QVBoxLayout();
        Layout_tree->setSpacing(6);
        Layout_tree->setObjectName(QString::fromUtf8("Layout_tree"));
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout->addItem(horizontalSpacer);

        CollapseAllButton = new QPushButton(WindowProfiler);
        CollapseAllButton->setObjectName(QString::fromUtf8("CollapseAllButton"));

        horizontalLayout->addWidget(CollapseAllButton);

        ExpandAllButton = new QPushButton(WindowProfiler);
        ExpandAllButton->setObjectName(QString::fromUtf8("ExpandAllButton"));

        horizontalLayout->addWidget(ExpandAllButton);


        Layout_tree->addLayout(horizontalLayout);

        tree_steps = new QTreeWidget(WindowProfiler);
        QTreeWidgetItem *__qtreewidgetitem = new QTreeWidgetItem();
        __qtreewidgetitem->setText(4, QString::fromUtf8("5"));
        __qtreewidgetitem->setText(3, QString::fromUtf8("4"));
        __qtreewidgetitem->setText(2, QString::fromUtf8("3"));
        __qtreewidgetitem->setText(1, QString::fromUtf8("2"));
        __qtreewidgetitem->setText(0, QString::fromUtf8("1"));
        tree_steps->setHeaderItem(__qtreewidgetitem);
        tree_steps->setObjectName(QString::fromUtf8("tree_steps"));
        tree_steps->setColumnCount(5);

        Layout_tree->addWidget(tree_steps);


        LayoutBottom->addLayout(Layout_tree);


        main_layout->addLayout(LayoutBottom);


        gridLayout->addLayout(main_layout, 0, 0, 1, 1);


        retranslateUi(WindowProfiler);

        QMetaObject::connectSlotsByName(WindowProfiler);
    } // setupUi

    void retranslateUi(QWidget *WindowProfiler)
    {
        WindowProfiler->setWindowTitle(QApplication::translate("WindowProfiler", "AdvancedTimer profiler window", nullptr));
        label_summary->setText(QApplication::translate("WindowProfiler", "Summary", nullptr));
        label_stepN->setText(QApplication::translate("WindowProfiler", "Step Number:", nullptr));
#ifndef QT_NO_TOOLTIP
        label_overhead->setToolTip(QApplication::translate("WindowProfiler", "Overhead due to the process of the timers. Close this window to avoid the overhead.", nullptr));
#endif // QT_NO_TOOLTIP
        label_overhead->setText(QApplication::translate("WindowProfiler", "Overhead (ms)", nullptr));
        label_stepValue->setText(QApplication::translate("WindowProfiler", "0", nullptr));
        label_time->setText(QApplication::translate("WindowProfiler", "Time (ms)", nullptr));
        label_timeValue->setText(QApplication::translate("WindowProfiler", "0", nullptr));
        label_overheadValue->setText(QApplication::translate("WindowProfiler", "0", nullptr));
#ifndef QT_NO_TOOLTIP
        label_timersCounter->setToolTip(QApplication::translate("WindowProfiler", "Number of timers in the current step", nullptr));
#endif // QT_NO_TOOLTIP
        label_timersCounter->setText(QApplication::translate("WindowProfiler", "Timers Counter:", nullptr));
        label_timersCounterValue->setText(QApplication::translate("WindowProfiler", "0", nullptr));
#ifndef QT_NO_TOOLTIP
        CollapseAllButton->setToolTip(QApplication::translate("WindowProfiler", "Collapse all", nullptr));
#endif // QT_NO_TOOLTIP
        CollapseAllButton->setText(QString());
#ifndef QT_NO_TOOLTIP
        ExpandAllButton->setToolTip(QApplication::translate("WindowProfiler", "Expand all", nullptr));
#endif // QT_NO_TOOLTIP
        ExpandAllButton->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class WindowProfiler: public Ui_WindowProfiler {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_WINDOWPROFILER_H
