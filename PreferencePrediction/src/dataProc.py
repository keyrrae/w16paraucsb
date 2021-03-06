from __future__ import print_function
from busiMR import Business
from busiMR import Restaurant
from busiMR import attributeAccumulatorParam
from reviewMR import Review
from userMR import User

import os
import itertools
import math

from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf() \
        .setAppName("YelpReviewALS") \
        .set("spark.executor.memory", "2g")\
        .set("spark.python.worker.memory", "2g")
    sc = SparkContext('local', conf=conf)

    businessRDD = sc.textFile("../../../data/yelp_academic_dataset_business.json")
    sc.setCheckpointDir("checkpoints/")
    restaurantRDD = businessRDD.map(Business.to_string).filter(Business.is_res)
    for item in businessRDD.take(10):
        print(item)
    restaurantList = restaurantRDD.map(Business.get_id).collect()

    restBC = sc.broadcast(restaurantList)

    if os.path.exists("RestaurantReviews"):
        os.system("rm -rf RestaurantReviews")

    reviewRDD = sc.textFile("../../../data/yelp_academic_dataset_review_large.json")\
        .filter(lambda x: Review.is_res(x, restBC))\
        .map(Review.parseRatings)\
        .saveAsTextFile("RestaurantReviews")
