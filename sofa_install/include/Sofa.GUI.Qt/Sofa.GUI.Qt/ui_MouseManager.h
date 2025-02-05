/********************************************************************************
** Form generated from reading UI file 'MouseManager.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MOUSEMANAGER_H
#define UI_MOUSEMANAGER_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QVBoxLayout>

QT_BEGIN_NAMESPACE

class Ui_MouseManager
{
public:
    QVBoxLayout *vboxLayout;
    QGroupBox *LeftButton;
    QVBoxLayout *vboxLayout1;
    QLabel *LeftOperationLabel;
    QComboBox *LeftOperationCombo;
    QGroupBox *MiddleButton;
    QVBoxLayout *vboxLayout2;
    QLabel *MiddleOperationLabel;
    QComboBox *MiddleOperationCombo;
    QGroupBox *RightButton;
    QVBoxLayout *vboxLayout3;
    QLabel *RightOperationLabel;
    QComboBox *RightOperationCombo;
    QSpacerItem *spacer2;

    void setupUi(QDialog *MouseManager)
    {
        if (MouseManager->objectName().isEmpty())
            MouseManager->setObjectName(QString::fromUtf8("MouseManager"));
        MouseManager->resize(295, 612);
        vboxLayout = new QVBoxLayout(MouseManager);
        vboxLayout->setSpacing(6);
        vboxLayout->setContentsMargins(11, 11, 11, 11);
        vboxLayout->setObjectName(QString::fromUtf8("vboxLayout"));
        LeftButton = new QGroupBox(MouseManager);
        LeftButton->setObjectName(QString::fromUtf8("LeftButton"));
        vboxLayout1 = new QVBoxLayout(LeftButton);
        vboxLayout1->setSpacing(6);
        vboxLayout1->setContentsMargins(11, 11, 11, 11);
        vboxLayout1->setObjectName(QString::fromUtf8("vboxLayout1"));
        LeftOperationLabel = new QLabel(LeftButton);
        LeftOperationLabel->setObjectName(QString::fromUtf8("LeftOperationLabel"));
        LeftOperationLabel->setWordWrap(false);

        vboxLayout1->addWidget(LeftOperationLabel);

        LeftOperationCombo = new QComboBox(LeftButton);
        LeftOperationCombo->setObjectName(QString::fromUtf8("LeftOperationCombo"));

        vboxLayout1->addWidget(LeftOperationCombo);


        vboxLayout->addWidget(LeftButton);

        MiddleButton = new QGroupBox(MouseManager);
        MiddleButton->setObjectName(QString::fromUtf8("MiddleButton"));
        vboxLayout2 = new QVBoxLayout(MiddleButton);
        vboxLayout2->setSpacing(6);
        vboxLayout2->setContentsMargins(11, 11, 11, 11);
        vboxLayout2->setObjectName(QString::fromUtf8("vboxLayout2"));
        MiddleOperationLabel = new QLabel(MiddleButton);
        MiddleOperationLabel->setObjectName(QString::fromUtf8("MiddleOperationLabel"));
        MiddleOperationLabel->setWordWrap(false);

        vboxLayout2->addWidget(MiddleOperationLabel);

        MiddleOperationCombo = new QComboBox(MiddleButton);
        MiddleOperationCombo->setObjectName(QString::fromUtf8("MiddleOperationCombo"));

        vboxLayout2->addWidget(MiddleOperationCombo);


        vboxLayout->addWidget(MiddleButton);

        RightButton = new QGroupBox(MouseManager);
        RightButton->setObjectName(QString::fromUtf8("RightButton"));
        vboxLayout3 = new QVBoxLayout(RightButton);
        vboxLayout3->setSpacing(6);
        vboxLayout3->setContentsMargins(11, 11, 11, 11);
        vboxLayout3->setObjectName(QString::fromUtf8("vboxLayout3"));
        RightOperationLabel = new QLabel(RightButton);
        RightOperationLabel->setObjectName(QString::fromUtf8("RightOperationLabel"));
        RightOperationLabel->setWordWrap(false);

        vboxLayout3->addWidget(RightOperationLabel);

        RightOperationCombo = new QComboBox(RightButton);
        RightOperationCombo->setObjectName(QString::fromUtf8("RightOperationCombo"));

        vboxLayout3->addWidget(RightOperationCombo);


        vboxLayout->addWidget(RightButton);

        spacer2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        vboxLayout->addItem(spacer2);


        retranslateUi(MouseManager);

        QMetaObject::connectSlotsByName(MouseManager);
    } // setupUi

    void retranslateUi(QDialog *MouseManager)
    {
        MouseManager->setWindowTitle(QApplication::translate("MouseManager", "MouseManager", nullptr));
        LeftButton->setTitle(QApplication::translate("MouseManager", "Left Button", nullptr));
        LeftOperationLabel->setText(QApplication::translate("MouseManager", "Operation:", nullptr));
        MiddleButton->setTitle(QApplication::translate("MouseManager", "Middle Button", nullptr));
        MiddleOperationLabel->setText(QApplication::translate("MouseManager", "Operation:", nullptr));
        RightButton->setTitle(QApplication::translate("MouseManager", "Right Button", nullptr));
        RightOperationLabel->setText(QApplication::translate("MouseManager", "Operation:", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MouseManager: public Ui_MouseManager {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MOUSEMANAGER_H
