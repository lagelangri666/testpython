from osgeo import gdal
import cv2
import numpy as np
import os

path = "G:/pythonfilecode/SoliDivide/SoilSort"
array_of_img = []
def read_directory(path):
    txt_file = open("soil.txt","w")
    for filename in os.listdir(path):
        img = cv_imread(path+"/"+filename)
        array_of_img.append(img)
        g = img[10,10,1]
        r = img[10,10,2]
        b = img[10,10,0]
        txt_file.write(str(filename)+"    "+str(r)+"    "+str(g)+"    "+str(b)+"\n")
    return 0;

def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img

soil_file = os.path.join(".","shp534.tif")
png_file = os.path.join(".","黄红壤.png")
RGB_file = os.path.join(".","RGB.tif")

img = cv_imread(png_file)
a = read_directory(path)

# img = cv2.imread(png_file,cv2.IMREAD_UNCHANGED)
# h,w,g =(img.shape)
# img_array = np.array(img)
# print(np.shape(img))
#
def read_tif(filename):
    dataset = gdal.Open(filename)
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()

    data = dataset.ReadAsArray(0,0,width,height)

    del dataset
    return data, im_geotrans,im_proj

def read_tif_2(filename):
    dataset = gdal.Open(filename)
    width = dataset.RasterXSize
    height = dataset.RasterYSize

    data = dataset.ReadAsArray(0,0,width,height)

    del dataset
    return data
def write_tif(filename, data):
    if 'int8' in data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    b, h, w = data.shape

    driver = gdal.GetDriverByName("GTiff")
    data_set = driver.Create(filename, w, h, b, datatype)

    for i  in range(b):
        data_set.GetRasterBand(i+1).WriteArray(data[i])

    del data_set
def write_tif2(filename,data,im_geotrans,im_proj):
    if 'int8' in data.dtype.name:
        print("int8")
        datatype = gdal.GDT_Byte
    elif 'int16' in data.dtype.name:
        datatype = gdal.GDT_UInt16
        print('int16')
    else:
        datatype = gdal.GDT_Float32
        print('float')

    if data.ndim == 3:
        band_nums, height, width = data.shape
    elif data.ndim == 2:
        band_nums = 1
        height, width = data.shape
    else:
        print("error: array dim!")

    #创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, width, height, band_nums, datatype)#数据类型必须有，需要计算内存空间
    dataset.SetGeoTransform(im_geotrans) #写入仿射变换参数
    dataset.SetProjection(im_proj) #写入地图投影信息

    for i in range(band_nums):
        dataset.GetRasterBand(i + 1).WriteArray(data[i])

    del dataset

if __name__ == "__main__":
    # flag_num = np.zeros(260,int)
    # data_soil = read_tif(soil_file)
    # RGB_img = np.zeros((data_soil.shape[0], data_soil.shape[1], 4), np.uint8)
    # for i in range(0,4096):
    #     print(i)
    #     for j in range(0,4096):
    #         #print(j)
    #         num = data_soil[i,j]
    #         if num != 256:
    #             rgb_data = [0,0,0,0]
    #             lnum = -1
    #             with open('soilDivide.txt', mode='r', encoding='gbk') as f:
    #                 for line in f.readlines():
    #                     lnum +=1
    #                     if(lnum == num):
    #                         cur_line = line.strip().split("    ")
    #                         rgb_data[0]=cur_line[1]
    #                         rgb_data[1] = cur_line[2]
    #                         rgb_data[2] = cur_line[3]
    #                         rgb_data[3] = cur_line[4]
    #                         RGB_img[i, j] = [rgb_data[0],rgb_data[1],rgb_data[2],rgb_data[3]]
    #                         break
    #         else :
    #             RGB_img[i, j] = [0, 0, 0, 256]

    # write_tif("RGB.tif", np.transpose(RGB_img, (2, 0, 1)))
    data_s, data_imgeo, data_impro =read_tif(soil_file)
    data_RGB = read_tif_2(RGB_file)
    print(data_RGB.shape)
    write_tif2("Soli_rgb.tif",data_RGB,data_imgeo,data_impro)
