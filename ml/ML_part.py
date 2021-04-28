#!/usr/bin/env python
# coding: utf-8
import pyspark.sql.types as typ
import pyspark.ml.evaluation as ev
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.ml.feature as ft
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pandas.plotting import scatter_matrix
import pandas as pd
import six
from pyspark.sql.functions import abs
import os

currentDir = os.getcwd()
lastDir = os.path.abspath(os.path.join(os.getcwd(), ".."))

# open data file
spark = SparkSession.builder.appName("Machine learning part").config("spark.some.config.option", "some-value").getOrCreate()

#df = spark.read.csv('file:///home/2020/spring/nyu/6513/xz2760/P2/data/Dataset_vehicles.csv', header = True)
df = spark.read.csv('file://'+ lastDir + '/data/Dataset_vehicles.csv', header = True)

# select the columns we want for the model
cols = ['price','year','manufacturer','model','odometer']
df = df.select(*cols)

# drop null values and change string data type to double type
df = df.na.drop()
df = df.withColumn("price", df["price"].cast(DoubleType()))
df = df.withColumn("year", df["year"].cast(DoubleType()))
df = df.withColumn("odometer", df["odometer"].cast(DoubleType()))

# modify data by subtracting 1900 from year and divide odometer by 5000
df = df.withColumn("year", df['year']-1900)
df = df.withColumn("odometer", df['odometer']/5000)

df.show()

# encode manufacturer and model by StringIndexer
encoder1 = ft.StringIndexer(inputCol='manufacturer', outputCol='manufacturer_VEC', handleInvalid="skip")
encoder2 = ft.StringIndexer(inputCol='model', outputCol='model_VEC', handleInvalid="skip")

# prepare the data for machine learning, we need only two columns, one is features and one is price
featuresCreator = ft.VectorAssembler(inputCols=['year', 'odometer', encoder1.getOutputCol(), encoder2.getOutputCol()], outputCol='features', handleInvalid="skip")

# define the feature columns and lable columns for linear regression model
lr = LinearRegression(featuresCol = featuresCreator.getOutputCol(), labelCol='price',maxIter=10, regParam=0.3, elasticNetParam=0.8)

# define the stages for pipeline
pipeline = Pipeline(stages = [encoder1, encoder2, featuresCreator, lr])

# split the training and testing dataset
df_train, df_test = df.randomSplit([0.7,0.3], seed = 123)

# put te training dataset into pipeline
model = pipeline.fit(df_train)

# test_model = model.transform(df_test)
# test_model = test_model.withColumn('prediction',abs(test_model.prediction))
# test_model.select("prediction","price","features").show(1000)

# print the rmse and r2 score
trainingSummary = model.stages[-1].summary
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)

# print the coefficients and intercept
print("Coefficients: " + str(model.stages[-1].coefficients))
print("Intercept: " + str(model.stages[-1].intercept))

# define the export table attributes
data = encoder1.fit(df).transform(df)
data1 = encoder2.fit(data).transform(data)
export1 = data1.select(['manufacturer','manufacturer_VEC'])
export2 = data1.select(['model','model_VEC'])
export1 = export1.toPandas()
export2 = export2.toPandas()
export1 = export1.drop_duplicates()
export2 = export2.drop_duplicates()

# export the tables to csv file to current folder
#export1.to_csv('/home/2020/spring/nyu/6513/xz2760/P2/ml/',index = False, header=True)
#export2.to_csv('/home/2020/spring/nyu/6513/xz2760/P2/ml/',index = False, header=True)
export1.to_csv(currentDir+'/manufacturer.csv',index = False, header=True)
export2.to_csv(currentDir+'/model.csv',index = False, header=True)

# show dataframe detail to pandas format
data1.describe().toPandas().transpose()

# use scatter matrix to roughly determine if there is a linear correlation between multiple independent variables
#numeric_features = [t[0] for t in data1.dtypes if t[1] == 'int' or t[1] == 'double']
#sampled_data = data1.select(numeric_features).sample(False, 0.8).toPandas()
#axs = scatter_matrix(sampled_data, figsize=(10, 10))
#n = len(sampled_data.columns)
#for i in range(n):
#    v = axs[i, 0]
#    v.yaxis.label.set_rotation(0)
#    v.yaxis.label.set_ha('right')
#    v.set_yticks(())
#    h = axs[n-1, i]
#    h.xaxis.label.set_rotation(90)
#    h.set_xticks(())

# calculate correlation between independent variables and target variable
for i in data1.columns:
    if not( isinstance(data1.select(i).take(1)[0][0], six.string_types)):
        print( "Correlation to price for ", i, data1.stat.corr('price',i))
