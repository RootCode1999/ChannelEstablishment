### 随机生成角度
import random,math
def calculateRandomDegree(x1,x2,y1,y2,z1,z2):
    # 计算两个点的水平方向（东-北方向）
    dx = x2 - x1
    dy = y2 - y1
    azimuth = math.atan2(dy, dx)  # atan2返回值的范围是-π到π
    azimuth_degrees_p = math.degrees(azimuth)  # 将弧度转换为度

    dx = x1-x2
    dy = y1-y2
    azimuth = math.atan2(dy, dx)  # atan2返回值的范围是-π到π
    azimuth_degrees_q = math.degrees(azimuth)  # 将弧度转换为度

    # 计算两个点的俯仰角
    dz = z2 - z1
    distance = math.sqrt(dx**2 + dy**2)
    elevation = math.atan2(dz, distance)  # 俯仰角
    elevation_degrees_p = math.degrees(elevation)  # 将弧度转换为度

    dz = z1 - z2
    distance = math.sqrt(dx**2 + dy**2)
    elevation = math.atan2(dz, distance)  # 俯仰角
    evalution_degrees_q = math.degrees(elevation)  # 将弧度转换为度

    return azimuth_degrees_p,elevation_degrees_p
def randomAngle():
    # 生成第一个点的坐标

    x1 = random.uniform(-10, 10)  # x坐标在-10到10之间
    y1 = random.uniform(-10, 10)  # y坐标在-10到10之间
    z1 = random.uniform(-10, 10)  # z坐标在-10到10之间

    # 生成第二个点的坐标
    x2 = random.uniform(-10, 10)  # x坐标在-10到10之间
    y2 = random.uniform(-10, 10)  # y坐标在-10到10之间
    z2 = random.uniform(-10, 10)  # z坐标在-10到10之间
    return calculateRandomDegree(x1,x2,y1,y2,z1,z2)

### 随机生成点簇
def randomCluster(x1,x2,y1,y2,z1,z2):
    cluster = []
    for i in range(10):
        cluster.append([])
    cluster[0].append([x1,y1,z1])
    for i in range(1,9):
        x = random.uniform(-10, 10)  # x坐标在-10到10之间
        y = random.uniform(-10, 10)  # y坐标在-10到10之间
        z = random.uniform(-10, 10)  # z坐标在-10到10之间
        cluster[i].append([x,y,z])
    cluster[9].append([x2,y2,z2])
    return cluster
