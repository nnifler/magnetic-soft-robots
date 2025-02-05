/********************************************************************************
** Form generated from reading UI file 'GUI.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_GUI_H
#define UI_GUI_H

#include <QtCore/QVariant>
#include <QtGui/QIcon>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QDockWidget>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include <sofa/gui/qt/config.h>

QT_BEGIN_NAMESPACE

class Ui_GUI
{
public:
    QAction *fileOpenAction;
    QAction *fileReloadAction;
    QAction *fileExitAction;
    QAction *helpAboutAction;
    QAction *ViewerAction;
    QAction *editRecordDirectoryAction;
    QAction *editGnuplotDirectoryAction;
    QAction *PluginManagerAction;
    QAction *MouseManagerAction;
    QAction *Action;
    QAction *TestAction;
    QAction *VideoRecorderManagerAction;
    QAction *helpShowDocBrowser;
    QAction *DataGraphAction;
    QWidget *widget;
    QVBoxLayout *vboxLayout;
    QHBoxLayout *mainWidgetLayout;
    QMenuBar *menubar;
    QMenu *fileMenu;
    QMenu *editMenu;
    QMenu *View;
    QMenu *helpMenu;
    QDockWidget *dockWidget;
    QWidget *dockWidgetContents;
    QHBoxLayout *horizontalLayout;
    QWidget *optionTabs;
    QVBoxLayout *_13;
    QGridLayout *_14;
    QPushButton *ResetViewButton;
    QPushButton *startButton;
    QPushButton *SaveViewButton;
    QPushButton *ReloadSceneButton;
    QPushButton *stepButton;
    QPushButton *screenshotButton;
    QHBoxLayout *_15;
    QLabel *dtLabel;
    QLineEdit *dtEdit;
    QCheckBox *realTimeCheckBox;
    QSpacerItem *spacer_tab;
    QTabWidget *tabs;
    QWidget *TabGraph;
    QVBoxLayout *_19;
    QHBoxLayout *horizontalLayout_2;
    QPushButton *ExportGraphButton;
    QPushButton *CollapseAllButton;
    QPushButton *ExpandAllButton;
    QPushButton *sceneGraphRefreshToggleButton;
    QWidget *tabView;
    QGridLayout *gridLayout1;
    QGridLayout *_17;
    QGridLayout *_18;
    QSpacerItem *spacer8;
    QLabel *pixmapLabel1;
    QSpacerItem *spacer7;
    QWidget *TabVisualGraph;
    QVBoxLayout *_20;
    QPushButton *ExportVisualGraphButton;
    QWidget *TabStats;
    QVBoxLayout *_21;
    QCheckBox *dumpStateCheckBox;
    QCheckBox *displayComputationTimeCheckBox;
    QCheckBox *exportGnuplotFilesCheckbox;
    QCheckBox *exportVisitorCheckbox;
    QCheckBox *displayTimeProfiler;
    QWidget *TabPage;
    QVBoxLayout *_22;
    QHBoxLayout *_23;
    QSpacerItem *spacer5_3_3;
    QSpinBox *sizeW;
    QLabel *textLabel_sizeX;
    QSpinBox *sizeH;
    QSpacerItem *spacer5_3_2_3;
    QTextBrowser *textEdit1;

    void setupUi(QMainWindow *GUI)
    {
        if (GUI->objectName().isEmpty())
            GUI->setObjectName(QString::fromUtf8("GUI"));
        GUI->resize(800, 600);
        QSizePolicy sizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(GUI->sizePolicy().hasHeightForWidth());
        GUI->setSizePolicy(sizePolicy);
        GUI->setMinimumSize(QSize(210, 481));
        GUI->setAcceptDrops(true);
        fileOpenAction = new QAction(GUI);
        fileOpenAction->setObjectName(QString::fromUtf8("fileOpenAction"));
        QIcon icon;
        icon.addFile(QString::fromUtf8("image3"), QSize(), QIcon::Normal, QIcon::Off);
        fileOpenAction->setIcon(icon);
        fileOpenAction->setProperty("name", QVariant(QByteArray("fileOpenAction")));
        fileReloadAction = new QAction(GUI);
        fileReloadAction->setObjectName(QString::fromUtf8("fileReloadAction"));
        fileReloadAction->setProperty("name", QVariant(QByteArray("fileReloadAction")));
        fileExitAction = new QAction(GUI);
        fileExitAction->setObjectName(QString::fromUtf8("fileExitAction"));
        fileExitAction->setProperty("name", QVariant(QByteArray("fileExitAction")));
        helpAboutAction = new QAction(GUI);
        helpAboutAction->setObjectName(QString::fromUtf8("helpAboutAction"));
        helpAboutAction->setEnabled(true);
        helpAboutAction->setIconVisibleInMenu(false);
        helpAboutAction->setProperty("name", QVariant(QByteArray("helpAboutAction")));
        ViewerAction = new QAction(GUI);
        ViewerAction->setObjectName(QString::fromUtf8("ViewerAction"));
        ViewerAction->setProperty("name", QVariant(QByteArray("ViewerAction")));
        editRecordDirectoryAction = new QAction(GUI);
        editRecordDirectoryAction->setObjectName(QString::fromUtf8("editRecordDirectoryAction"));
        editRecordDirectoryAction->setProperty("name", QVariant(QByteArray("editRecordDirectoryAction")));
        editGnuplotDirectoryAction = new QAction(GUI);
        editGnuplotDirectoryAction->setObjectName(QString::fromUtf8("editGnuplotDirectoryAction"));
        editGnuplotDirectoryAction->setProperty("name", QVariant(QByteArray("editGnuplotDirectoryAction")));
        PluginManagerAction = new QAction(GUI);
        PluginManagerAction->setObjectName(QString::fromUtf8("PluginManagerAction"));
        PluginManagerAction->setProperty("name", QVariant(QByteArray("PluginManagerAction")));
        MouseManagerAction = new QAction(GUI);
        MouseManagerAction->setObjectName(QString::fromUtf8("MouseManagerAction"));
        MouseManagerAction->setProperty("name", QVariant(QByteArray("MouseManagerAction")));
        Action = new QAction(GUI);
        Action->setObjectName(QString::fromUtf8("Action"));
        Action->setProperty("name", QVariant(QByteArray("Action")));
        TestAction = new QAction(GUI);
        TestAction->setObjectName(QString::fromUtf8("TestAction"));
        TestAction->setProperty("name", QVariant(QByteArray("TestAction")));
        VideoRecorderManagerAction = new QAction(GUI);
        VideoRecorderManagerAction->setObjectName(QString::fromUtf8("VideoRecorderManagerAction"));
        VideoRecorderManagerAction->setProperty("name", QVariant(QByteArray("VideoRecorderManagerAction")));
        helpShowDocBrowser = new QAction(GUI);
        helpShowDocBrowser->setObjectName(QString::fromUtf8("helpShowDocBrowser"));
        helpShowDocBrowser->setCheckable(false);
        helpShowDocBrowser->setIconVisibleInMenu(false);
        DataGraphAction = new QAction(GUI);
        DataGraphAction->setObjectName(QString::fromUtf8("DataGraphAction"));
        widget = new QWidget(GUI);
        widget->setObjectName(QString::fromUtf8("widget"));
        QSizePolicy sizePolicy1(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(widget->sizePolicy().hasHeightForWidth());
        widget->setSizePolicy(sizePolicy1);
        widget->setMinimumSize(QSize(0, 0));
        vboxLayout = new QVBoxLayout(widget);
        vboxLayout->setSpacing(2);
        vboxLayout->setContentsMargins(5, 5, 5, 5);
        vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
        vboxLayout->setSizeConstraint(QLayout::SetNoConstraint);
        vboxLayout->setContentsMargins(0, 0, 0, 0);
        mainWidgetLayout = new QHBoxLayout();
        mainWidgetLayout->setSpacing(2);
        mainWidgetLayout->setObjectName(QString::fromUtf8("mainWidgetLayout"));

        vboxLayout->addLayout(mainWidgetLayout);

        GUI->setCentralWidget(widget);
        menubar = new QMenuBar(GUI);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setEnabled(true);
        menubar->setGeometry(QRect(0, 0, 800, 22));
        fileMenu = new QMenu(menubar);
        fileMenu->setObjectName(QString::fromUtf8("fileMenu"));
        editMenu = new QMenu(menubar);
        editMenu->setObjectName(QString::fromUtf8("editMenu"));
        View = new QMenu(menubar);
        View->setObjectName(QString::fromUtf8("View"));
        helpMenu = new QMenu(menubar);
        helpMenu->setObjectName(QString::fromUtf8("helpMenu"));
        GUI->setMenuBar(menubar);
        dockWidget = new QDockWidget(GUI);
        dockWidget->setObjectName(QString::fromUtf8("dockWidget"));
        QSizePolicy sizePolicy2(QSizePolicy::Minimum, QSizePolicy::Expanding);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(dockWidget->sizePolicy().hasHeightForWidth());
        dockWidget->setSizePolicy(sizePolicy2);
        dockWidget->setMinimumSize(QSize(200, 551));
        dockWidgetContents = new QWidget();
        dockWidgetContents->setObjectName(QString::fromUtf8("dockWidgetContents"));
        sizePolicy2.setHeightForWidth(dockWidgetContents->sizePolicy().hasHeightForWidth());
        dockWidgetContents->setSizePolicy(sizePolicy2);
        dockWidgetContents->setMinimumSize(QSize(200, 0));
        horizontalLayout = new QHBoxLayout(dockWidgetContents);
        horizontalLayout->setSpacing(2);
        horizontalLayout->setContentsMargins(5, 5, 5, 5);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        optionTabs = new QWidget(dockWidgetContents);
        optionTabs->setObjectName(QString::fromUtf8("optionTabs"));
        optionTabs->setEnabled(true);
        sizePolicy1.setHeightForWidth(optionTabs->sizePolicy().hasHeightForWidth());
        optionTabs->setSizePolicy(sizePolicy1);
        _13 = new QVBoxLayout(optionTabs);
        _13->setSpacing(2);
        _13->setContentsMargins(5, 5, 5, 5);
        _13->setObjectName(QString::fromUtf8("_13"));
        _13->setSizeConstraint(QLayout::SetNoConstraint);
        _14 = new QGridLayout();
        _14->setSpacing(2);
        _14->setObjectName(QString::fromUtf8("_14"));
        _14->setSizeConstraint(QLayout::SetNoConstraint);
        ResetViewButton = new QPushButton(optionTabs);
        ResetViewButton->setObjectName(QString::fromUtf8("ResetViewButton"));
        ResetViewButton->setEnabled(true);

        _14->addWidget(ResetViewButton, 2, 0, 1, 1);

        startButton = new QPushButton(optionTabs);
        startButton->setObjectName(QString::fromUtf8("startButton"));
        startButton->setCheckable(true);

        _14->addWidget(startButton, 0, 0, 1, 1);

        SaveViewButton = new QPushButton(optionTabs);
        SaveViewButton->setObjectName(QString::fromUtf8("SaveViewButton"));
        SaveViewButton->setEnabled(true);

        _14->addWidget(SaveViewButton, 2, 1, 1, 1);

        ReloadSceneButton = new QPushButton(optionTabs);
        ReloadSceneButton->setObjectName(QString::fromUtf8("ReloadSceneButton"));
        ReloadSceneButton->setEnabled(true);

        _14->addWidget(ReloadSceneButton, 1, 0, 1, 1);

        stepButton = new QPushButton(optionTabs);
        stepButton->setObjectName(QString::fromUtf8("stepButton"));
        stepButton->setAutoRepeat(true);

        _14->addWidget(stepButton, 0, 1, 1, 1);

        screenshotButton = new QPushButton(optionTabs);
        screenshotButton->setObjectName(QString::fromUtf8("screenshotButton"));

        _14->addWidget(screenshotButton, 3, 0, 1, 2);

        _15 = new QHBoxLayout();
        _15->setSpacing(2);
        _15->setObjectName(QString::fromUtf8("_15"));
        _15->setSizeConstraint(QLayout::SetNoConstraint);
        dtLabel = new QLabel(optionTabs);
        dtLabel->setObjectName(QString::fromUtf8("dtLabel"));
        dtLabel->setWordWrap(false);

        _15->addWidget(dtLabel);

        dtEdit = new QLineEdit(optionTabs);
        dtEdit->setObjectName(QString::fromUtf8("dtEdit"));
        QSizePolicy sizePolicy3(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy3.setHorizontalStretch(0);
        sizePolicy3.setVerticalStretch(0);
        sizePolicy3.setHeightForWidth(dtEdit->sizePolicy().hasHeightForWidth());
        dtEdit->setSizePolicy(sizePolicy3);
        dtEdit->setMinimumSize(QSize(20, 0));
        dtEdit->setMaximumSize(QSize(80, 32767));

        _15->addWidget(dtEdit);

        realTimeCheckBox = new QCheckBox(optionTabs);
        realTimeCheckBox->setObjectName(QString::fromUtf8("realTimeCheckBox"));

        _15->addWidget(realTimeCheckBox);


        _14->addLayout(_15, 1, 1, 1, 1);


        _13->addLayout(_14);

        spacer_tab = new QSpacerItem(20, 8, QSizePolicy::Minimum, QSizePolicy::Fixed);

        _13->addItem(spacer_tab);

        tabs = new QTabWidget(optionTabs);
        tabs->setObjectName(QString::fromUtf8("tabs"));
        sizePolicy1.setHeightForWidth(tabs->sizePolicy().hasHeightForWidth());
        tabs->setSizePolicy(sizePolicy1);
        tabs->setMinimumSize(QSize(200, 0));
        TabGraph = new QWidget();
        TabGraph->setObjectName(QString::fromUtf8("TabGraph"));
        _19 = new QVBoxLayout(TabGraph);
        _19->setSpacing(2);
        _19->setContentsMargins(5, 5, 5, 5);
        _19->setObjectName(QString::fromUtf8("_19"));
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(2);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        ExportGraphButton = new QPushButton(TabGraph);
        ExportGraphButton->setObjectName(QString::fromUtf8("ExportGraphButton"));
        sizePolicy3.setHeightForWidth(ExportGraphButton->sizePolicy().hasHeightForWidth());
        ExportGraphButton->setSizePolicy(sizePolicy3);
        QIcon icon1;
        icon1.addFile(QString::fromUtf8("image1"), QSize(), QIcon::Normal, QIcon::Off);
        ExportGraphButton->setIcon(icon1);

        horizontalLayout_2->addWidget(ExportGraphButton);

        CollapseAllButton = new QPushButton(TabGraph);
        CollapseAllButton->setObjectName(QString::fromUtf8("CollapseAllButton"));
        CollapseAllButton->setStyleSheet(QString::fromUtf8(""));

        horizontalLayout_2->addWidget(CollapseAllButton);

        ExpandAllButton = new QPushButton(TabGraph);
        ExpandAllButton->setObjectName(QString::fromUtf8("ExpandAllButton"));
        ExpandAllButton->setStyleSheet(QString::fromUtf8(""));

        horizontalLayout_2->addWidget(ExpandAllButton);

        sceneGraphRefreshToggleButton = new QPushButton(TabGraph);
        sceneGraphRefreshToggleButton->setObjectName(QString::fromUtf8("sceneGraphRefreshToggleButton"));

        horizontalLayout_2->addWidget(sceneGraphRefreshToggleButton);


        _19->addLayout(horizontalLayout_2);

        tabs->addTab(TabGraph, QString());
        tabView = new QWidget();
        tabView->setObjectName(QString::fromUtf8("tabView"));
        sizePolicy1.setHeightForWidth(tabView->sizePolicy().hasHeightForWidth());
        tabView->setSizePolicy(sizePolicy1);
        gridLayout1 = new QGridLayout(tabView);
        gridLayout1->setSpacing(2);
        gridLayout1->setContentsMargins(5, 5, 5, 5);
        gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
        _17 = new QGridLayout();
        _17->setSpacing(2);
        _17->setObjectName(QString::fromUtf8("_17"));
        _18 = new QGridLayout();
        _18->setSpacing(2);
        _18->setObjectName(QString::fromUtf8("_18"));
        spacer8 = new QSpacerItem(0, 16, QSizePolicy::Ignored, QSizePolicy::Minimum);

        _18->addItem(spacer8, 0, 2, 1, 1);

        pixmapLabel1 = new QLabel(tabView);
        pixmapLabel1->setObjectName(QString::fromUtf8("pixmapLabel1"));
        QSizePolicy sizePolicy4(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy4.setHorizontalStretch(0);
        sizePolicy4.setVerticalStretch(0);
        sizePolicy4.setHeightForWidth(pixmapLabel1->sizePolicy().hasHeightForWidth());
        pixmapLabel1->setSizePolicy(sizePolicy4);
        pixmapLabel1->setPixmap(QPixmap(QString::fromUtf8("image0")));
        pixmapLabel1->setScaledContents(true);
        pixmapLabel1->setWordWrap(false);

        _18->addWidget(pixmapLabel1, 0, 1, 1, 1);

        spacer7 = new QSpacerItem(0, 16, QSizePolicy::Ignored, QSizePolicy::Minimum);

        _18->addItem(spacer7, 0, 0, 1, 1);


        _17->addLayout(_18, 1, 0, 1, 1);


        gridLayout1->addLayout(_17, 2, 0, 1, 1);

        tabs->addTab(tabView, QString());
        TabVisualGraph = new QWidget();
        TabVisualGraph->setObjectName(QString::fromUtf8("TabVisualGraph"));
        _20 = new QVBoxLayout(TabVisualGraph);
        _20->setSpacing(2);
        _20->setContentsMargins(5, 5, 5, 5);
        _20->setObjectName(QString::fromUtf8("_20"));
        ExportVisualGraphButton = new QPushButton(TabVisualGraph);
        ExportVisualGraphButton->setObjectName(QString::fromUtf8("ExportVisualGraphButton"));
        ExportVisualGraphButton->setIcon(icon1);

        _20->addWidget(ExportVisualGraphButton);

        tabs->addTab(TabVisualGraph, QString());
        TabStats = new QWidget();
        TabStats->setObjectName(QString::fromUtf8("TabStats"));
        _21 = new QVBoxLayout(TabStats);
        _21->setSpacing(2);
        _21->setContentsMargins(5, 5, 5, 5);
        _21->setObjectName(QString::fromUtf8("_21"));
        dumpStateCheckBox = new QCheckBox(TabStats);
        dumpStateCheckBox->setObjectName(QString::fromUtf8("dumpStateCheckBox"));

        _21->addWidget(dumpStateCheckBox);

        displayComputationTimeCheckBox = new QCheckBox(TabStats);
        displayComputationTimeCheckBox->setObjectName(QString::fromUtf8("displayComputationTimeCheckBox"));

        _21->addWidget(displayComputationTimeCheckBox);

        exportGnuplotFilesCheckbox = new QCheckBox(TabStats);
        exportGnuplotFilesCheckbox->setObjectName(QString::fromUtf8("exportGnuplotFilesCheckbox"));

        _21->addWidget(exportGnuplotFilesCheckbox);

        exportVisitorCheckbox = new QCheckBox(TabStats);
        exportVisitorCheckbox->setObjectName(QString::fromUtf8("exportVisitorCheckbox"));

        _21->addWidget(exportVisitorCheckbox);

        displayTimeProfiler = new QCheckBox(TabStats);
        displayTimeProfiler->setObjectName(QString::fromUtf8("displayTimeProfiler"));

        _21->addWidget(displayTimeProfiler);

        tabs->addTab(TabStats, QString());
        TabPage = new QWidget();
        TabPage->setObjectName(QString::fromUtf8("TabPage"));
        _22 = new QVBoxLayout(TabPage);
        _22->setSpacing(2);
        _22->setContentsMargins(5, 5, 5, 5);
        _22->setObjectName(QString::fromUtf8("_22"));
        _23 = new QHBoxLayout();
        _23->setSpacing(0);
        _23->setObjectName(QString::fromUtf8("_23"));
        spacer5_3_3 = new QSpacerItem(10, 2, QSizePolicy::Expanding, QSizePolicy::Minimum);

        _23->addItem(spacer5_3_3);

        sizeW = new QSpinBox(TabPage);
        sizeW->setObjectName(QString::fromUtf8("sizeW"));
        sizeW->setMaximum(30000);
        sizeW->setValue(800);

        _23->addWidget(sizeW);

        textLabel_sizeX = new QLabel(TabPage);
        textLabel_sizeX->setObjectName(QString::fromUtf8("textLabel_sizeX"));
        QSizePolicy sizePolicy5(QSizePolicy::Fixed, QSizePolicy::Preferred);
        sizePolicy5.setHorizontalStretch(0);
        sizePolicy5.setVerticalStretch(0);
        sizePolicy5.setHeightForWidth(textLabel_sizeX->sizePolicy().hasHeightForWidth());
        textLabel_sizeX->setSizePolicy(sizePolicy5);
        textLabel_sizeX->setWordWrap(false);

        _23->addWidget(textLabel_sizeX);

        sizeH = new QSpinBox(TabPage);
        sizeH->setObjectName(QString::fromUtf8("sizeH"));
        sizeH->setMaximum(30000);
        sizeH->setValue(600);

        _23->addWidget(sizeH);

        spacer5_3_2_3 = new QSpacerItem(10, 2, QSizePolicy::Expanding, QSizePolicy::Minimum);

        _23->addItem(spacer5_3_2_3);


        _22->addLayout(_23);

        textEdit1 = new QTextBrowser(TabPage);
        textEdit1->setObjectName(QString::fromUtf8("textEdit1"));

        _22->addWidget(textEdit1);

        tabs->addTab(TabPage, QString());

        _13->addWidget(tabs);


        horizontalLayout->addWidget(optionTabs);

        dockWidget->setWidget(dockWidgetContents);
        GUI->addDockWidget(static_cast<Qt::DockWidgetArea>(1), dockWidget);

        menubar->addAction(fileMenu->menuAction());
        menubar->addAction(editMenu->menuAction());
        menubar->addAction(View->menuAction());
        menubar->addAction(helpMenu->menuAction());
        fileMenu->addAction(fileOpenAction);
        fileMenu->addAction(fileReloadAction);
        fileMenu->addSeparator();
        fileMenu->addSeparator();
        fileMenu->addAction(fileExitAction);
        editMenu->addAction(editRecordDirectoryAction);
        editMenu->addAction(editGnuplotDirectoryAction);
        editMenu->addSeparator();
        editMenu->addAction(PluginManagerAction);
        editMenu->addAction(MouseManagerAction);
        editMenu->addAction(VideoRecorderManagerAction);
        editMenu->addAction(DataGraphAction);
        View->addSeparator();
        View->addSeparator();
        View->addSeparator();
        helpMenu->addSeparator();
        helpMenu->addAction(helpShowDocBrowser);
        helpMenu->addAction(helpAboutAction);

        retranslateUi(GUI);
        QObject::connect(fileOpenAction, SIGNAL(triggered()), GUI, SLOT(popupOpenFileSelector()));
        QObject::connect(fileReloadAction, SIGNAL(triggered()), GUI, SLOT(fileReload()));
        QObject::connect(fileExitAction, SIGNAL(triggered()), GUI, SLOT(fileExit()));
        QObject::connect(editRecordDirectoryAction, SIGNAL(triggered()), GUI, SLOT(editRecordDirectory()));
        QObject::connect(PluginManagerAction, SIGNAL(triggered()), GUI, SLOT(showPluginManager()));
        QObject::connect(MouseManagerAction, SIGNAL(triggered()), GUI, SLOT(showMouseManager()));
        QObject::connect(DataGraphAction, SIGNAL(triggered()), GUI, SLOT(showWindowDataGraph()));
        QObject::connect(editGnuplotDirectoryAction, SIGNAL(triggered()), GUI, SLOT(editGnuplotDirectory()));
        QObject::connect(VideoRecorderManagerAction, SIGNAL(triggered()), GUI, SLOT(showVideoRecorderManager()));
        QObject::connect(helpShowDocBrowser, SIGNAL(triggered()), GUI, SLOT(showDocBrowser()));

        tabs->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(GUI);
    } // setupUi

    void retranslateUi(QMainWindow *GUI)
    {
        GUI->setWindowTitle(QApplication::translate("GUI", "Sofa", nullptr));
        fileOpenAction->setText(QApplication::translate("GUI", "&Open...", nullptr));
        fileOpenAction->setIconText(QApplication::translate("GUI", "Open", nullptr));
#ifndef QT_NO_SHORTCUT
        fileOpenAction->setShortcut(QApplication::translate("GUI", "Ctrl+O", nullptr));
#endif // QT_NO_SHORTCUT
        fileReloadAction->setText(QApplication::translate("GUI", "&Reload", nullptr));
        fileReloadAction->setIconText(QApplication::translate("GUI", "Reload", nullptr));
#ifndef QT_NO_SHORTCUT
        fileReloadAction->setShortcut(QApplication::translate("GUI", "Ctrl+R", nullptr));
#endif // QT_NO_SHORTCUT
        fileExitAction->setText(QApplication::translate("GUI", "E&xit", nullptr));
        fileExitAction->setIconText(QApplication::translate("GUI", "Exit", nullptr));
#ifndef QT_NO_SHORTCUT
        fileExitAction->setShortcut(QString());
#endif // QT_NO_SHORTCUT
        helpAboutAction->setText(QApplication::translate("GUI", "&About", nullptr));
        helpAboutAction->setIconText(QApplication::translate("GUI", "About", nullptr));
#ifndef QT_NO_SHORTCUT
        helpAboutAction->setShortcut(QString());
#endif // QT_NO_SHORTCUT
        ViewerAction->setIconText(QApplication::translate("GUI", "Viewer", nullptr));
        editRecordDirectoryAction->setText(QApplication::translate("GUI", "Record Directory...", nullptr));
        editRecordDirectoryAction->setIconText(QApplication::translate("GUI", "Record Directory...", nullptr));
        editGnuplotDirectoryAction->setText(QApplication::translate("GUI", "Gnuplot Directory...", nullptr));
        editGnuplotDirectoryAction->setIconText(QApplication::translate("GUI", "Gnuplot Directory...", nullptr));
        PluginManagerAction->setText(QApplication::translate("GUI", "Plugin Manager...", nullptr));
        PluginManagerAction->setIconText(QApplication::translate("GUI", "Plugin Manager...", nullptr));
        MouseManagerAction->setText(QApplication::translate("GUI", "Mouse Manager...", nullptr));
        MouseManagerAction->setIconText(QApplication::translate("GUI", "Mouse Manager...", nullptr));
        Action->setIconText(QApplication::translate("GUI", "Recently Opened Files...", nullptr));
        TestAction->setText(QApplication::translate("GUI", "Test", nullptr));
        TestAction->setIconText(QApplication::translate("GUI", "Test", nullptr));
        VideoRecorderManagerAction->setText(QApplication::translate("GUI", "Video Recorder Manager...", nullptr));
        VideoRecorderManagerAction->setIconText(QApplication::translate("GUI", "Video Recorder Manager...", nullptr));
        helpShowDocBrowser->setText(QApplication::translate("GUI", "Show doc browser", nullptr));
        DataGraphAction->setText(QApplication::translate("GUI", "Data Graph...", nullptr));
#ifndef QT_NO_TOOLTIP
        DataGraphAction->setToolTip(QApplication::translate("GUI", "Data Graph Window", nullptr));
#endif // QT_NO_TOOLTIP
        fileMenu->setTitle(QApplication::translate("GUI", "&File", nullptr));
        editMenu->setTitle(QApplication::translate("GUI", "&Edit", nullptr));
        View->setTitle(QApplication::translate("GUI", "&View", nullptr));
        helpMenu->setTitle(QApplication::translate("GUI", "Help", nullptr));
#ifndef QT_NO_TOOLTIP
        ResetViewButton->setToolTip(QApplication::translate("GUI", "Set the camera to initial position and orientation", nullptr));
#endif // QT_NO_TOOLTIP
        ResetViewButton->setText(QApplication::translate("GUI", "Reset &View", nullptr));
#ifndef QT_NO_SHORTCUT
        ResetViewButton->setShortcut(QApplication::translate("GUI", "Alt+V", nullptr));
#endif // QT_NO_SHORTCUT
#ifndef QT_NO_TOOLTIP
        startButton->setToolTip(QApplication::translate("GUI", "Launch the Simulation", nullptr));
#endif // QT_NO_TOOLTIP
        startButton->setText(QApplication::translate("GUI", "&Animate", nullptr));
#ifndef QT_NO_SHORTCUT
        startButton->setShortcut(QApplication::translate("GUI", "Alt+A", nullptr));
#endif // QT_NO_SHORTCUT
#ifndef QT_NO_TOOLTIP
        SaveViewButton->setToolTip(QApplication::translate("GUI", "Save the position and orientation of the camera", nullptr));
#endif // QT_NO_TOOLTIP
        SaveViewButton->setText(QApplication::translate("GUI", "Save Vie&w", nullptr));
#ifndef QT_NO_SHORTCUT
        SaveViewButton->setShortcut(QApplication::translate("GUI", "Alt+W", nullptr));
#endif // QT_NO_SHORTCUT
#ifndef QT_NO_TOOLTIP
        ReloadSceneButton->setToolTip(QApplication::translate("GUI", "Reload the simulation file", nullptr));
#endif // QT_NO_TOOLTIP
        ReloadSceneButton->setText(QApplication::translate("GUI", "&Reload Scene", nullptr));
#ifndef QT_NO_SHORTCUT
        ReloadSceneButton->setShortcut(QApplication::translate("GUI", "Alt+R", nullptr));
#endif // QT_NO_SHORTCUT
#ifndef QT_NO_TOOLTIP
        stepButton->setToolTip(QApplication::translate("GUI", "Compute the simulation at time t+DT", nullptr));
#endif // QT_NO_TOOLTIP
        stepButton->setText(QApplication::translate("GUI", "S&tep", nullptr));
#ifndef QT_NO_SHORTCUT
        stepButton->setShortcut(QApplication::translate("GUI", "Alt+T", nullptr));
#endif // QT_NO_SHORTCUT
        screenshotButton->setText(QApplication::translate("GUI", "Save S&creenshot", nullptr));
#ifndef QT_NO_SHORTCUT
        screenshotButton->setShortcut(QApplication::translate("GUI", "Alt+C", nullptr));
#endif // QT_NO_SHORTCUT
        dtLabel->setText(QApplication::translate("GUI", "DT:", nullptr));
#ifndef QT_NO_TOOLTIP
        realTimeCheckBox->setToolTip(QApplication::translate("GUI", "Use the duration of the previous simulation step as the next DT", nullptr));
#endif // QT_NO_TOOLTIP
        realTimeCheckBox->setText(QApplication::translate("GUI", "Real Time", nullptr));
        ExportGraphButton->setText(QApplication::translate("GUI", "Export Graph...", nullptr));
#ifndef QT_NO_SHORTCUT
        ExportGraphButton->setShortcut(QApplication::translate("GUI", "Alt+X", nullptr));
#endif // QT_NO_SHORTCUT
#ifndef QT_NO_TOOLTIP
        CollapseAllButton->setToolTip(QApplication::translate("GUI", "Collapse All", nullptr));
#endif // QT_NO_TOOLTIP
        CollapseAllButton->setText(QString());
#ifndef QT_NO_TOOLTIP
        ExpandAllButton->setToolTip(QApplication::translate("GUI", "Expand All", nullptr));
#endif // QT_NO_TOOLTIP
        ExpandAllButton->setText(QString());
#ifndef QT_NO_TOOLTIP
        sceneGraphRefreshToggleButton->setToolTip(QApplication::translate("GUI", "The scene graph update button has three states\n"
"State 0: unlocked (all the changes on the graph are immediately taken into account)\n"
"State 1: locked (the changes on the graph are not done but the simulation graph is set to dirty if\n"
"         there is some changes on the graph. A click on the button unlocks the graph (go to state 0).\n"
"State 2: dirty, in that state the button reflect the fact that the scene graph view has changed but not displayed.\n"
"         A click on the button refreshes the graph view but does not change the Lock/Unlock state", nullptr));
#endif // QT_NO_TOOLTIP
        sceneGraphRefreshToggleButton->setText(QString());
        tabs->setTabText(tabs->indexOf(TabGraph), QApplication::translate("GUI", "Graph", nullptr));
#ifndef QT_NO_TOOLTIP
        pixmapLabel1->setToolTip(QApplication::translate("GUI", "http://sofa-framework.org", nullptr));
#endif // QT_NO_TOOLTIP
        tabs->setTabText(tabs->indexOf(tabView), QApplication::translate("GUI", "View", nullptr));
        ExportVisualGraphButton->setText(QApplication::translate("GUI", "E&xport Graph...", nullptr));
#ifndef QT_NO_SHORTCUT
        ExportVisualGraphButton->setShortcut(QApplication::translate("GUI", "Alt+X", nullptr));
#endif // QT_NO_SHORTCUT
        tabs->setTabText(tabs->indexOf(TabVisualGraph), QApplication::translate("GUI", "Visual", nullptr));
#ifndef QT_NO_TOOLTIP
        dumpStateCheckBox->setToolTip(QApplication::translate("GUI", "Record the state at each time step in file \"dumpState.data\"", "This is used to plut curves fter a simulation"));
#endif // QT_NO_TOOLTIP
        dumpStateCheckBox->setText(QApplication::translate("GUI", "Dump State", nullptr));
#ifndef QT_NO_TOOLTIP
        displayComputationTimeCheckBox->setToolTip(QApplication::translate("GUI", "Display information about the time spent at each branch of the graph", nullptr));
#endif // QT_NO_TOOLTIP
        displayComputationTimeCheckBox->setText(QApplication::translate("GUI", "Log Time", nullptr));
#ifndef QT_NO_TOOLTIP
        exportGnuplotFilesCheckbox->setToolTip(QApplication::translate("GUI", "Create gnuplot files for each named element of the simulation", nullptr));
#endif // QT_NO_TOOLTIP
        exportGnuplotFilesCheckbox->setText(QApplication::translate("GUI", "Export state as gnuplot files", nullptr));
#ifndef QT_NO_TOOLTIP
        exportVisitorCheckbox->setToolTip(QApplication::translate("GUI", "Open a Dialog showing a trace of the execution and time spent", nullptr));
#endif // QT_NO_TOOLTIP
        exportVisitorCheckbox->setText(QApplication::translate("GUI", "Trace Visitor and Component execution", nullptr));
        displayTimeProfiler->setText(QApplication::translate("GUI", "Display AdvancedTimer profiler", nullptr));
        tabs->setTabText(tabs->indexOf(TabStats), QApplication::translate("GUI", "Stats", nullptr));
        textLabel_sizeX->setText(QApplication::translate("GUI", "<p align=\"center\">x</p>", nullptr));
        tabs->setTabText(tabs->indexOf(TabPage), QApplication::translate("GUI", "Viewer", nullptr));
    } // retranslateUi

};

namespace Ui {
    class GUI: public Ui_GUI {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_GUI_H
