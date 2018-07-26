import random


def shops(shop):
    data = {
    "id": shop.id,
     "shop_name": shop.shop_name,
     "shop_img": "http://www.homework.com/images/shop-logo.png",
     "shop_rating": shop.shop_rating,
     "brand": shop.is_brand,
     "on_time": shop.is_ontime,
     "fengniao": shop.is_bird,
     "bao": shop.is_bao,
     "piao": shop.is_fp,
     "zhun": shop.is_zun,
     "start_send": shop.start_cost,
     "send_cost": shop.send_cost,
     "distance": random.randint(100,1000),
     "estimate_time": 30,
     "notice": shop.notice,
     "discount": shop.discount
    }
    return data


def shop_view(shop):
    data={
        "id": shop.id,
        "shop_name": shop.shop_name,
        "shop_img": "http://www.homework.com/images/shop-logo.png",
        "shop_rating": shop.shop_rating,
        "service_code": 4.6,
        "foods_code": 4.4,
        "high_or_low": True,
        "h_l_percent": 30,
        "brand": shop.is_brand,
        "on_time": shop.is_ontime,
        "fengniao": shop.is_bird,
        "bao": shop.is_bao,
        "piao": shop.is_fp,
        "zhun": shop.is_zun,
        "start_send":  shop.start_cost,
        "send_cost": shop.send_cost,
        "distance": random.randint(100,1000),
        "estimate_time": 30,
        "notice": shop.notice,
        "discount": shop.discount,
        "evaluate": [{
                "user_id": 12344,
                "username": "w******k",
                "user_img": "http://www.homework.com/images/slider-pic4.jpeg",
                "time": "2017-2-22",
                "evaluate_code": 1,
                "send_time": 30,
                "evaluate_details": "不怎么好吃"
            },
            {
                "user_id": 12344,
                "username": "w******k",
                "user_img": "http://www.homework.com/images/slider-pic4.jpeg",
                "time": "2017-2-22",
                "evaluate_code": 4.5,
                "send_time": 30,
                "evaluate_details": "很好吃"
            },
            {
                "user_id": 12344,
                "username": "w******k",
                "user_img": "http://www.homework.com/images/slider-pic4.jpeg",
                "time": "2017-2-22",
                "evaluate_code": 5,
                "send_time": 30,
                "evaluate_details": "很好吃"
            },
            {
                "user_id": 12344,
                "username": "w******k",
                "user_img": "http://www.homework.com/images/slider-pic4.jpeg",
                "time": "2017-2-22",
                "evaluate_code": 4.7,
                "send_time": 30,
                "evaluate_details": "很好吃"
            },
            {
                "user_id": 12344,
                "username": "w******k",
                "user_img": "http://www.homework.com/images/slider-pic4.jpeg",
                "time": "2017-2-22",
                "evaluate_code": 5,
                "send_time": 30,
                "evaluate_details": "很好吃"
            }
        ],
        "commodity": [{
                "description": c. description,
                "is_selected": c.is_default,
                "name": c.name,
                "type_accumulation": "c"+str(c.id),
                "goods_list": [{
                        "goods_id": f.id,
                        "goods_name": f.food_name,
                        "rating": f.rating,
                        "goods_price": float(f.food_price),
                        "description": f.description,
                        "month_sales": f.month_sales,
                        "rating_count": f.rating_count,
                        "tips": f.tips,
                        "satisfy_count": 8,
                        "satisfy_rate": 95,
                        "goods_img": "http://www.homework.com/images/slider-pic4.jpeg"
                    }for f in c.foods]
            } for c in shop.categories]


    }
    return data























































































































































































































































































































































































































































































































































































































































