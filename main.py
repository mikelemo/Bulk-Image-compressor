import os
import sys
import io

# Serialization module
import yaml

from PyQt5 import QtWidgets

# Dark style platte module
import qdarkstyle

from PyQt5.QtCore import QSize, Qt, QUrl, QBuffer
from PyQt5.QtGui import QIcon, QImage, QPixmap, QStandardItemModel
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QSpinBox,
    QToolBar,
    QVBoxLayout,
    QListView,
    QListWidgetItem,
)

from PyQt5 import uic


from PIL import Image
from PIL import ImageQt


def QImage2PILImage(img):
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_im = Image.open(io.BytesIO(buffer.data()))
    return pil_im


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI form
        uic.loadUi("gui/form.ui", self)

        self.show()

        self.ImgPaths = []

        self.ImgLabels = []
        self.ImgItems = []

        self.ImgsBuff = []
        self.ImgsMBuff = []

        self.FPaths = []

        self.ImgPreviewSize = QSize(600, 400)

        for x in range(10):
            self.ImgLabels.append(QLabel(self))
            self.ImgsMBuff.append(QImage())
            self.ImgsBuff.append(QImage())
            # self.ImgItems.append(Q)

        self.img_buff = []

        # Load Configurations
        conf_params = {'KRatio':0, 'ResX':0, 'ResY':0, 'Res':"", 'NameExt':"", 'ExportPath':"", 'Path':"",
                'Quality':40, 'ColorMode':"RGB", 'Threshold': 50}


        # Apply configurations

        
        self.ImgQualitySpinBox.setValue(conf_params['Quality'])
                
        # with open("app_config.yml", "w") as f:

        #     # if conf_params['Res'] is not "Not Found":  
        #     print("Initializing YAML file") 
        #     yaml.dump(conf_params, f)


        with open("app_config.yml", "r") as f:
            
            print("Read YAML params")
            conf_params = yaml.load(f, Loader=yaml.FullLoader)


            # else: 
        
        print(conf_params['Res'])


        # ------------------- Connect my actions -----------------------
        # Connect load file to open file action
        
        self.loadBtn.clicked.connect(self.open_file)
        self.ExportBtn.clicked.connect(self.setExportPath)

        self.ExportFilesBtn.clicked.connect(self.saveImgs)

        self.SaveConfBtn.clicked.connect(self.saveConfig)

        self.NewResComboBox.currentIndexChanged.connect(self.convertImgs)
        self.ColorModeComboBox.currentIndexChanged.connect(self.convertImgs)

        self.NewXResLineEdit.editingFinished.connect(self.convertImgs)
        self.NewYResLineEdit.editingFinished.connect(self.convertImgs)

        self.actionOpen.triggered.connect(self.open_file)

        # Setup Imgs view box
        self.ImgsView.setViewMode(QListView.IconMode)
        self.ImgsView.setIconSize(QSize(100, 75))
        self.ImgsView.setGridSize(QSize(120, 100))

        # self.model = QStandardItemModel()
        # self.ImgsView.setModel(self.model)



    # ----------------- Main Class Functions ------------------------

    def loadImgBuffer(self):
        pass

    def convertImgs(self):
        
        # Display all images in thumbnail grid( With names and selectability)

        # Filter options:
        # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#PIL.Image.LANCZOS

        # self.im_resized = im.resize((1280, 720), Image.LANCZOS)
        # self.im_resized.save((folderpath+"/Compressed_"+filename), optimize=True,quality=30) 

        # Different conversion modes:
        # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
        
        # ----------------Save converted images--------------

        # Pure black and white:

        # thresh = 200
        # fn = lambda x : 255 if x > thresh else 0
        # blk_img = self.im_resized.convert('L').point(fn, mode='1')
        # blk_img.save((folderpath+"/Black_"+filename), optimize=True,quality=30)

        # grayscaled = self.im_resized.convert('L') # 'L' -  (8-bit pixels, mapped to any other mode using a color palette)
        # grayscaled.save((folderpath+"/Gray_"+filename), optimize=True,quality=30)
        print("Converting images!")

        print("Clearing QWidgetView Items")

        NewImgRes = []
        if self.NewResComboBox.currentText() == "Custom":
            NewImgRes.append(self.NewXResLineEdit.text())
            NewImgRes.append(self.NewYResLineEdit.text())
        else:
            NewImgRes = self.NewResComboBox.currentText().split('*')
        
        self.ImgsMBuff = []

        ColorMode = self.ColorModeComboBox.currentText()

        self.BulkFileSize = 0
        for idx, img in enumerate(self.ImgsBuff):
            # img = img.convertToFormat(QImage.Format_Grayscale8)

            # file_size = os.path.getsize(self.ImgsBuff[idx].FilePath)
            file_size = os.path.getsize(self.FPaths[idx])
            file_size_mb = (file_size/1024)/1024
            # self.ImgsMBuff.append(img.scaled(int(NewImgRes[0]), int(NewImgRes[1]), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.ImgsMBuff.append(img.scaled(int(NewImgRes[0]), int(NewImgRes[1]), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            if ColorMode == "GrayScale":

                self.ImgsMBuff[idx] = self.ImgsMBuff[idx].convertToFormat(QImage.Format_Grayscale16)

            elif ColorMode == "Monochrome":

                 self.ImgsMBuff[idx] = self.ImgsMBuff[idx].convertToFormat(QImage.Format_Mono)


            else:
                print("RGB Color export")
            # Convert ImgsMBuff to to pi with PIL's fromImage() convert to black and white with
            # threshhold and convert back to QImage        

            print(f"New File Size: {file_size_mb}MB, Img Size: {NewImgRes}")

            
            # ---------Set current image file size label
            
            self.FinaleFileSizeLabel.setText(str(round((self.ImgsMBuff[idx].sizeInBytes()/1024/1024), 3)) + "MB")

            print(f"Finale File Size: {self.ImgsMBuff[idx].sizeInBytes()}")
            # Update preview image

            self.img_resized = QPixmap.fromImage(self.ImgsMBuff[0])

            self.ReviewImg.setPixmap(self.img_resized.scaled(self.ImgPreviewSize.width(),
                self.ImgPreviewSize.height(), aspectRatioMode=Qt.KeepAspectRatio))
        
        # self.FinaleBulkFileSizeLabel.setText(str(round(self.BulkFileSize, 3)) + "MB")
            
    def saveImgs(self):

        if os.path.isdir(self.ExportFolderPath):
            for idx, img in enumerate(self.ImgsMBuff):

                filename = os.path.basename(self.FPaths[idx]).split('.')[0]
                NewFileName = f"{self.ExportFolderPath}/{filename}{self.NameExtBox.displayText()}.jpg"
                print("Saving: " + NewFileName)
                img.save(NewFileName, quality = self.ImgQualitySpinBox.value())

                self.statusBar().showMessage("Files Exported!")

        # thresh = 200
        # fn = lambda x : 255 if x > thresh else 0
        # blk_img = self.im_resized.convert('L').point(fn, mode='1')
        # # blk_img.save((folderpath+"/Black_"+filename), optimize=True,quality=30)

        # grayscaled = self.im_resized.convert('L') # 'L' -  (8-bit pixels, mapped to any other mode using a color palette)
        # # grayscaled.save((folderpath+"/Gray_"+filename), optimize=True,quality=30)
    

        else:
            print("Error: No export path")
            self.statusBar().showMessage("Failed to export")
        


    def setExportPath(self):
        
        self.ExportFolderPath = QFileDialog.getExistingDirectory(self, 'Select Folder !')
        self.ExportPathBox.setText(self.ExportFolderPath)
        self.statusBar().showMessage(f"Set Export Path: {self.ExportFolderPath}")
        


    def saveConfig(self):

        self.statusBar().showMessage("Configurations saved!")
        

    def open_file(self):

        FilePaths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open file",
            "./images",
            "Image Format(*.jpg *.jpeg *.png *.bmp);;" "All files (*.*)",
        )

        self.ImgPaths = FilePaths

        self.ExportFolderPath = os.path.dirname(os.path.abspath(FilePaths[0]))
        self.ExportPathBox.setText(self.ExportFolderPath)

        print(FilePaths)



        if FilePaths:

            # Iterate over file paths 
            self.ImgsMBuff = []
            self.ImgsBuff = []
            self.ImgsThumbBuff = []
            self.ThumBuff = []

            self.FPaths = []

            self.ImgsView.clear()

            for idx, img_path in enumerate(FilePaths):

                self.ImgsBuff.insert(idx, QImage(img_path))

                # self.ImgsThumbBuff.append(self.ImgsBuff[idx].scaled(800, 600).scaled(100, 75, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                # self.ImgsBuff[idx].FilePath = img_path

                self.FPaths.append(img_path)

                # self.self.ImgsBuff[idx] = Image.open(img_path)
                filename = os.path.basename(img_path)
                print(filename)
                folderpath = os.path.dirname(os.path.abspath(img_path))

                print(f"The image size dimensions are: {self.ImgsBuff[idx].width()}*{self.ImgsBuff[idx].height()}")

                # Display all images in thumbnail grid( With names and selectability)
                # Filter options:
                # https://pillow.readthedocs.io/en/stable/handbook/concepts.html#PIL.Image.LANCZOS

                self.ImgsThumbBuff.append(QListWidgetItem(QIcon(img_path), filename))
                # self.model.appendRow(self.ImgsThumbBuff[idx])
                self.ImgsView.addItem(self.ImgsThumbBuff[idx])

                FilePath = FilePaths[0]

                im = Image.open(FilePath)
                filename = os.path.basename(FilePath)
                print(filename)
                folderpath = os.path.dirname(os.path.abspath(FilePath))

                self.filePathTextBox.setText(FilePath)
                print(f"The image size dimensions are: {im.size}")

                self.ImgXSizeLabel.setText(str(im.size[0]) + 'px')
                self.ImgYSizeLabel.setText(str(im.size[1]) + 'px')
                
                # Get image file size:
                file_size = os.path.getsize(FilePath)
                file_size_mb = (file_size/1024)/1024
                self.BulkFileSize = 0
                self.BulkFileSize += file_size_mb

                print(f"Image file size = {(file_size/1024)/1024} MB")
                self.FileSizeLabel.setText (str(round(file_size_mb, 3))+ " MB") 

                try: 
                    ImgRatio = (im.size[0])/(im.size[1])
                except ValueError:
                    print("Something is wrong")

                self.RatioLabel.setText(str(round(ImgRatio, 3)))
                # self.img_resized = QPixmap.fromImage(self.ImgsBuff[0])

                self.originalImg = QPixmap(self.ImgsBuff[0])

                # self.OrigImg.resize(self.ImgPreviewSize)
                self.OrigImg.setPixmap(self.originalImg.scaled(self.ImgPreviewSize.width(),
                    self.ImgPreviewSize.height(), aspectRatioMode=Qt.KeepAspectRatio))

                # Will update teh Review image there
                self.convertImgs()

                self.statusBar().showMessage("Loaded File.")
            else:
                self.statusBar().showMessage("Open Files aborted")

app = QApplication(sys.argv)
app.setApplicationName("My Image Resizer")
app.setOrganizationName("Q-Link")
app.setOrganizationDomain("www.Q-link.site")

window = MainWindow()

window.setWindowTitle("Image resizer V0.8")
# window.setWindowState(Qt.WindowMaximized) # WindowFullScreen

# Setup Dark stylesheet:
app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

app.exec_()
