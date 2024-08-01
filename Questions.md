OreRestaurant
Miss Ore is a restaurant owner and she is looking to have an online presence for her restaurant;
where people can order from her store, make enquiries, and also, importantly, where her staff
can add, remove, and update the menu.
She is looking forward to OreRestaurant v0.1 where the below needs are met.
Using a python/PHP backend framework of your choosing, create a backend system for Ore.
● Staff can Create, Delete, and Update the food menu. Customers cannot do any of these
actions.
● Customers should be able to see the list of menus and be capable of retrieving a
particular item on the menu.
● Staff can retrieve the number of (Registered) Customers.
● Staff can access the list of Registered Customers; A Customer cannot. There should be
a clear error message if a Customer attempts to see this list: “You do not have the
permission to access this resource,” for example.
● Customers can place an order and Staff can see placed orders.
/users endpoint: staff can retrieve all registered users
/users/<:id> endpoint: staff can retrieve a particular user
/profile endpoint: authenticated user can see their profile information
/menus endpoint: user can retrieve all menus
/menus/<:id> endpoint: user can retrieve a particular menu
/menus/discounted endpoint: user can see menus on discount
/menus/drinks endpoint: user can see all drinks on the menu
Food Delivery/Carryout only runs from 10AM to 6PM.*
Do note that Ore has a bit of experience in programming and she believes a project such as this
would have good use of comments to explain certain code lines/blocks and the use of tests. You
may wow Ore with additional features you think would be beneficial to her store.
Deploy your project on a FREE platform in order to avoid incurring any cost.
NB: You are expected to submit this task on or before 11:59pm Thursday 1st August,
2024