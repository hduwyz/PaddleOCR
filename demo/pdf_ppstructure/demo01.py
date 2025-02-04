import datetime
import os
import fitz  # fitz就是pip install PyMuPDF
import cv2
from tools import test_hubserving


def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为4，这将为我们生成分辨率提高4的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 4  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 4
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf转图片时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


pdfDir = './pdf'


def gci(filepath):
    # 遍历filepath下所有文件
    files = os.listdir(filepath)
    for fi in files:
        # 将转换的图片保存到对应imgs的对应子目录下
        pyMuPDF_fitz(os.path.join(filepath, fi), os.path.join('imgs', fi[:-4]))


if __name__ == '__main__':
    filepath = r'./data/'
    # gci(filepath)
    image = cv2.imread('./imgs/test/images_4.png')
    result = test_hubserving.main(r'http://127.0.0.1:8866/predict/ocr_system', r'./imgs/test/')
