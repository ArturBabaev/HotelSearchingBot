<h1 align="center">HotelSearchingBot</h1>

Bot for searching hotels on the site hotels.com

<h3 align="left">Packages:</h>

<h4 align="left">a) botrequests:</h>

1) city_req - Function for determining the city id;
2) hotels_req - Hotel search function by city id;
3) photo_req -  Photo search function by hotel id;

<h4 align="left">b) controllers:</h>

1) bestdeal_controller - Best deal request processing class;
2) help_controller - Help request processing class;
3) history_controller - History request processing class;
4) price_controller - Price request processing class;
5) start_controller - Start request processing class;

<h4 align="left">c) model:</h>

1) history - Class describing the history;
2) user - Class describing the user;

<h4 align="left">d) repository:</h>

1) db_helper - Database tables creation class;
2) history_repository - Database history table entry class;
3) user_repository - Database user table entry class;

<h4 align="left">e) service:</h>

1) bestdeal - Sort hotels by distance from center and price;
2) checkphoto - Check for the required number of photos;
3) ending - Required ending;
4) highprice - Sort hotels from highest to lowest price;
5) lowprice - Sorting hotels from lowest to highest price.