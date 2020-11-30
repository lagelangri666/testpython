from osgeo import gdal
import numpy as np
import cv2
import os

# path = ['LC08_L1TP_123039_20150619_20170407_01_T1', 'LC08_L1TP_123039_20150806_20170406_01_T1', 'LC08_L1TP_123039_20150923_20170403_01_T1',
#         'LC08_L1TP_123039_20161128_20180523_01_T1', 'LC08_L1TP_123039_20180203_20180220_01_T1', 'LC08_L1TP_123039_20180713_20180717_01_T1',
#         'LC08_L1TP_123039_20190716_20190721_01_T1', 'LC08_L1TP_123039_20190902_20190916_01_T1']
path = ['LC08_L1TP_123039_20181017_20181030_01_T1']
def read_tif(imgpath):
    dataset = gdal.Open(imgpath)

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息

    width = dataset.RasterXSize
    height = dataset.RasterYSize

    data = dataset.ReadAsArray(0, 0, width, height)

    del dataset
    return data, im_geotrans, im_proj

def write_tif(filename, data, im_geotrans, im_proj):
    # gdal数据类型包括
    # gdal.GDT_Byte,
    # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    # gdal.GDT_Float32, gdal.GDT_Float64

    # 判断栅格数据的数据类型
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
    # dataset.SetGeoTransform(im_geotrans) #写入仿射变换参数
    # dataset.SetProjection(im_proj) #写入地图投影信息

    for i in range(band_nums):
        dataset.GetRasterBand(i + 1).WriteArray(data)

    del dataset

def zmMinFilterGray(src, r=7):
    '''最小值滤波，r是滤波器半径'''
    return cv2.erode(src, np.ones((2 * r + 1, 2 * r + 1)))

# def guidedfilter(I, p, r, eps):
#     '''''引导滤波，直接参考网上的matlab代码'''
#     height, width = I.shape
#     m_I = cv2.boxFilter(I, -1, (r, r))
#     m_p = cv2.boxFilter(p, -1, (r, r))
#     m_Ip = cv2.boxFilter(I * p, -1, (r, r))
#     cov_Ip = m_Ip - m_I * m_p
#
#     m_II = cv2.boxFilter(I * I, -1, (r, r))
#     var_I = m_II - m_I * m_I
#
#     a = cov_Ip / (var_I + eps)
#     b = m_p - a * m_I
#
#     m_a = cv2.boxFilter(a, -1, (r, r))
#     m_b = cv2.boxFilter(b, -1, (r, r))
#     return m_a * I + m_b

def dark_channel(m):                 # 输入rgb图像，值范围[0,1]
    V1 = np.min(m, 0)                           # 得到暗通道图像
    Dark_Channel = zmMinFilterGray(V1, 1)
    # cv2.imshow('20190708_Dark', Dark_Channel)    # 查看暗通道
    # cv2.waitKey(0)
    return Dark_Channel

if __name__ == "__main__":
    # img_path = '20181017_band_432.tif'
    # out_path = 'dark_1.tif'
    for _path in path:
        img_path = os.path.join('.', 'data', _path, _path)
        # img_path = os.path.join('.', 'test', _path, _path)
        _path = os.path.join('.', 'data', _path, 'test', _path)
        # data, im_geotrans, im_proj = read_tif(img_path)
        # print(im_geotrans, '----', im_proj)
        # dark_data = dark_channel(data)
        # write_tif(out_path, dark_data, im_geotrans, im_proj)
        #
        out_path = os.path.join(_path + '_Dark2346.tif')
        data1, im_geotrans1, im_proj1 = read_tif(img_path+'_B2.tif')
        data2, im_geotrans2, im_proj2 = read_tif(img_path+'_B3.tif')
        data3, im_geotrans3, im_proj3 = read_tif(img_path+'_B4.tif')
        data4, im_geotrans4, im_proj4 = read_tif(img_path+'_B6.tif')
        data = np.zeros((4, data1.shape[0], data1.shape[1]), dtype=np.uint16)
        data[0] = data1
        data[1] = data2
        data[2] = data3
        data[3] = data4
        dark_data = dark_channel(data)
        write_tif(out_path, dark_data, im_geotrans1, im_proj1)
