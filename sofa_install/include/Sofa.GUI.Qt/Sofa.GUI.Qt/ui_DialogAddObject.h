/********************************************************************************
** Form generated from reading UI file 'DialogAddObject.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_DIALOGADDOBJECT_H
#define UI_DIALOGADDOBJECT_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSpacerItem>

QT_BEGIN_NAMESPACE

class Ui_DialogAddObject
{
public:
    QGridLayout *gridLayout;
    QHBoxLayout *hboxLayout;
    QLabel *scaleText;
    QLineEdit *scaleValue;
    QHBoxLayout *hboxLayout1;
    QLabel *openFileText;
    QLineEdit *openFilePath;
    QPushButton *openFileButton;
    QHBoxLayout *hboxLayout2;
    QSpacerItem *Horizontal_Spacing2;
    QPushButton *buttonOk;
    QPushButton *buttonCancel;
    QHBoxLayout *hboxLayout3;
    QLabel *positionText;
    QLineEdit *positionX;
    QLineEdit *positionY;
    QLineEdit *positionZ;
    QHBoxLayout *hboxLayout4;
    QLabel *rotationText;
    QLineEdit *rotationX;
    QLineEdit *rotationY;
    QLineEdit *rotationZ;
    QGroupBox *buttonGroup;
    QGridLayout *gridLayout1;
    QRadioButton *custom;

    void setupUi(QDialog *DialogAddObject)
    {
        if (DialogAddObject->objectName().isEmpty())
            DialogAddObject->setObjectName(QString::fromUtf8("DialogAddObject"));
        DialogAddObject->resize(556, 264);
        QSizePolicy sizePolicy(QSizePolicy::Ignored, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(DialogAddObject->sizePolicy().hasHeightForWidth());
        DialogAddObject->setSizePolicy(sizePolicy);
        DialogAddObject->setSizeGripEnabled(true);
        gridLayout = new QGridLayout(DialogAddObject);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        hboxLayout = new QHBoxLayout();
        hboxLayout->setSpacing(6);
        hboxLayout->setObjectName(QString::fromUtf8("hboxLayout"));
        scaleText = new QLabel(DialogAddObject);
        scaleText->setObjectName(QString::fromUtf8("scaleText"));
        scaleText->setWordWrap(false);

        hboxLayout->addWidget(scaleText);

        scaleValue = new QLineEdit(DialogAddObject);
        scaleValue->setObjectName(QString::fromUtf8("scaleValue"));

        hboxLayout->addWidget(scaleValue);


        gridLayout->addLayout(hboxLayout, 4, 0, 1, 1);

        hboxLayout1 = new QHBoxLayout();
        hboxLayout1->setSpacing(6);
        hboxLayout1->setObjectName(QString::fromUtf8("hboxLayout1"));
        openFileText = new QLabel(DialogAddObject);
        openFileText->setObjectName(QString::fromUtf8("openFileText"));
        openFileText->setWordWrap(false);

        hboxLayout1->addWidget(openFileText);

        openFilePath = new QLineEdit(DialogAddObject);
        openFilePath->setObjectName(QString::fromUtf8("openFilePath"));

        hboxLayout1->addWidget(openFilePath);

        openFileButton = new QPushButton(DialogAddObject);
        openFileButton->setObjectName(QString::fromUtf8("openFileButton"));

        hboxLayout1->addWidget(openFileButton);


        gridLayout->addLayout(hboxLayout1, 1, 0, 1, 1);

        hboxLayout2 = new QHBoxLayout();
        hboxLayout2->setSpacing(6);
        hboxLayout2->setObjectName(QString::fromUtf8("hboxLayout2"));
        Horizontal_Spacing2 = new QSpacerItem(20, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout2->addItem(Horizontal_Spacing2);

        buttonOk = new QPushButton(DialogAddObject);
        buttonOk->setObjectName(QString::fromUtf8("buttonOk"));
        buttonOk->setAutoDefault(true);

        hboxLayout2->addWidget(buttonOk);

        buttonCancel = new QPushButton(DialogAddObject);
        buttonCancel->setObjectName(QString::fromUtf8("buttonCancel"));
        buttonCancel->setAutoDefault(true);

        hboxLayout2->addWidget(buttonCancel);


        gridLayout->addLayout(hboxLayout2, 5, 0, 1, 1);

        hboxLayout3 = new QHBoxLayout();
        hboxLayout3->setSpacing(6);
        hboxLayout3->setObjectName(QString::fromUtf8("hboxLayout3"));
        positionText = new QLabel(DialogAddObject);
        positionText->setObjectName(QString::fromUtf8("positionText"));
        positionText->setWordWrap(false);

        hboxLayout3->addWidget(positionText);

        positionX = new QLineEdit(DialogAddObject);
        positionX->setObjectName(QString::fromUtf8("positionX"));

        hboxLayout3->addWidget(positionX);

        positionY = new QLineEdit(DialogAddObject);
        positionY->setObjectName(QString::fromUtf8("positionY"));

        hboxLayout3->addWidget(positionY);

        positionZ = new QLineEdit(DialogAddObject);
        positionZ->setObjectName(QString::fromUtf8("positionZ"));

        hboxLayout3->addWidget(positionZ);


        gridLayout->addLayout(hboxLayout3, 2, 0, 1, 1);

        hboxLayout4 = new QHBoxLayout();
        hboxLayout4->setSpacing(6);
        hboxLayout4->setObjectName(QString::fromUtf8("hboxLayout4"));
        rotationText = new QLabel(DialogAddObject);
        rotationText->setObjectName(QString::fromUtf8("rotationText"));
        rotationText->setWordWrap(false);

        hboxLayout4->addWidget(rotationText);

        rotationX = new QLineEdit(DialogAddObject);
        rotationX->setObjectName(QString::fromUtf8("rotationX"));

        hboxLayout4->addWidget(rotationX);

        rotationY = new QLineEdit(DialogAddObject);
        rotationY->setObjectName(QString::fromUtf8("rotationY"));

        hboxLayout4->addWidget(rotationY);

        rotationZ = new QLineEdit(DialogAddObject);
        rotationZ->setObjectName(QString::fromUtf8("rotationZ"));

        hboxLayout4->addWidget(rotationZ);


        gridLayout->addLayout(hboxLayout4, 3, 0, 1, 1);

        buttonGroup = new QGroupBox(DialogAddObject);
        buttonGroup->setObjectName(QString::fromUtf8("buttonGroup"));
        gridLayout1 = new QGridLayout(buttonGroup);
        gridLayout1->setSpacing(6);
        gridLayout1->setContentsMargins(11, 11, 11, 11);
        gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
        custom = new QRadioButton(buttonGroup);
        custom->setObjectName(QString::fromUtf8("custom"));

        gridLayout1->addWidget(custom, 0, 0, 1, 1);


        gridLayout->addWidget(buttonGroup, 0, 0, 1, 1);


        retranslateUi(DialogAddObject);
        QObject::connect(openFileButton, SIGNAL(clicked()), DialogAddObject, SLOT(fileOpen()));
        QObject::connect(buttonOk, SIGNAL(clicked()), DialogAddObject, SLOT(accept()));
        QObject::connect(buttonCancel, SIGNAL(clicked()), DialogAddObject, SLOT(reject()));

        buttonOk->setDefault(true);


        QMetaObject::connectSlotsByName(DialogAddObject);
    } // setupUi

    void retranslateUi(QDialog *DialogAddObject)
    {
        DialogAddObject->setWindowTitle(QApplication::translate("DialogAddObject", "Add a scene or an object", nullptr));
        scaleText->setText(QApplication::translate("DialogAddObject", "Scale", nullptr));
        openFileText->setText(QApplication::translate("DialogAddObject", "Open File", nullptr));
        openFileButton->setText(QString());
        buttonOk->setText(QApplication::translate("DialogAddObject", "&OK", nullptr));
#ifndef QT_NO_SHORTCUT
        buttonOk->setShortcut(QString());
#endif // QT_NO_SHORTCUT
        buttonCancel->setText(QApplication::translate("DialogAddObject", "&Cancel", nullptr));
#ifndef QT_NO_SHORTCUT
        buttonCancel->setShortcut(QString());
#endif // QT_NO_SHORTCUT
        positionText->setText(QApplication::translate("DialogAddObject", "Initial Position", nullptr));
        rotationText->setText(QApplication::translate("DialogAddObject", "Initial Rotation", nullptr));
        buttonGroup->setTitle(QApplication::translate("DialogAddObject", "Objects", nullptr));
        custom->setText(QApplication::translate("DialogAddObject", "custom", nullptr));
    } // retranslateUi

};

namespace Ui {
    class DialogAddObject: public Ui_DialogAddObject {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_DIALOGADDOBJECT_H
