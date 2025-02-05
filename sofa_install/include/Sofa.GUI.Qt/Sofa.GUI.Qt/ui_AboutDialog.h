/********************************************************************************
** Form generated from reading UI file 'AboutDialog.ui'
**
** Created by: Qt User Interface Compiler version 5.12.12
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ABOUTDIALOG_H
#define UI_ABOUTDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>

QT_BEGIN_NAMESPACE

class Ui_AboutDialog
{
public:
    QGridLayout *gridLayout;
    QGroupBox *buttonGroup;
    QGridLayout *gridLayout1;
    QLabel *label;
    QLabel *label_3;
    QLabel *label_2;
    QHBoxLayout *hboxLayout;
    QSpacerItem *Horizontal_Spacing2;
    QPushButton *buttonOk;
    QSpacerItem *horizontalSpacer;
    QLabel *label_4;

    void setupUi(QDialog *AboutDialog)
    {
        if (AboutDialog->objectName().isEmpty())
            AboutDialog->setObjectName(QString::fromUtf8("AboutDialog"));
        AboutDialog->setEnabled(true);
        AboutDialog->resize(464, 543);
        QSizePolicy sizePolicy(QSizePolicy::Ignored, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(AboutDialog->sizePolicy().hasHeightForWidth());
        AboutDialog->setSizePolicy(sizePolicy);
        AboutDialog->setSizeGripEnabled(false);
        AboutDialog->setModal(false);
        gridLayout = new QGridLayout(AboutDialog);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setSizeConstraint(QLayout::SetFixedSize);
        buttonGroup = new QGroupBox(AboutDialog);
        buttonGroup->setObjectName(QString::fromUtf8("buttonGroup"));
        buttonGroup->setAlignment(Qt::AlignCenter);
        buttonGroup->setFlat(false);
        gridLayout1 = new QGridLayout(buttonGroup);
        gridLayout1->setSpacing(6);
        gridLayout1->setContentsMargins(11, 11, 11, 11);
        gridLayout1->setObjectName(QString::fromUtf8("gridLayout1"));
        label = new QLabel(buttonGroup);
        label->setObjectName(QString::fromUtf8("label"));
        label->setMinimumSize(QSize(0, 0));
        label->setScaledContents(false);
        label->setWordWrap(true);

        gridLayout1->addWidget(label, 1, 0, 1, 1);

        label_3 = new QLabel(buttonGroup);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setTextFormat(Qt::AutoText);
        label_3->setWordWrap(true);

        gridLayout1->addWidget(label_3, 3, 0, 1, 1);

        label_2 = new QLabel(buttonGroup);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setMinimumSize(QSize(0, 0));
        label_2->setLayoutDirection(Qt::LeftToRight);
        label_2->setTextFormat(Qt::PlainText);
        label_2->setAlignment(Qt::AlignCenter);
        label_2->setWordWrap(false);
        label_2->setMargin(0);

        gridLayout1->addWidget(label_2, 2, 0, 1, 1);


        gridLayout->addWidget(buttonGroup, 1, 0, 2, 1);

        hboxLayout = new QHBoxLayout();
        hboxLayout->setSpacing(6);
        hboxLayout->setObjectName(QString::fromUtf8("hboxLayout"));
        Horizontal_Spacing2 = new QSpacerItem(20, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout->addItem(Horizontal_Spacing2);

        buttonOk = new QPushButton(AboutDialog);
        buttonOk->setObjectName(QString::fromUtf8("buttonOk"));
        buttonOk->setMinimumSize(QSize(150, 40));
        buttonOk->setAutoRepeat(false);
        buttonOk->setAutoDefault(true);
        buttonOk->setFlat(false);

        hboxLayout->addWidget(buttonOk);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        hboxLayout->addItem(horizontalSpacer);


        gridLayout->addLayout(hboxLayout, 5, 0, 1, 1);

        label_4 = new QLabel(AboutDialog);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setAlignment(Qt::AlignCenter);
        label_4->setWordWrap(true);

        gridLayout->addWidget(label_4, 0, 0, 1, 1);


        retranslateUi(AboutDialog);
        QObject::connect(buttonOk, SIGNAL(clicked()), AboutDialog, SLOT(accept()));

        buttonOk->setDefault(true);


        QMetaObject::connectSlotsByName(AboutDialog);
    } // setupUi

    void retranslateUi(QDialog *AboutDialog)
    {
        AboutDialog->setWindowTitle(QApplication::translate("AboutDialog", "About", nullptr));
        buttonGroup->setTitle(QString());
#ifndef QT_NO_ACCESSIBILITY
        label->setAccessibleDescription(QString());
#endif // QT_NO_ACCESSIBILITY
        label->setText(QApplication::translate("AboutDialog", "SOFA is an open-source framework for interactive physics simulation, with an emphasis on soft body dynamics. After years of research and development, the project remains open-source under the LGPL v2.1 license, fostering both research and development.", nullptr));
        label_3->setText(QApplication::translate("AboutDialog", "Open-source is kept thriving thanks to partners supporting us: be part of the community and get involved your own way!", nullptr));
#ifndef QT_NO_ACCESSIBILITY
        label_2->setAccessibleDescription(QString());
#endif // QT_NO_ACCESSIBILITY
        label_2->setText(QString());
        buttonOk->setText(QApplication::translate("AboutDialog", "Support us", nullptr));
        label_4->setText(QApplication::translate("AboutDialog", "SOFA, Simulation Open-Framework Architecture                                (c) 2006 INRIA, USTL, UJF, CNRS, MGH", nullptr));
    } // retranslateUi

};

namespace Ui {
    class AboutDialog: public Ui_AboutDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ABOUTDIALOG_H
