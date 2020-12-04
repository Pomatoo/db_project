# db_project
1. Automation script: (in progress)
    - create instances (done)
    - attach security group (done)
    - sh script to install packages and setup configuration (MySQL,MongoDB) (done)
    - load dataset from get_data.sh (done)
    - hadoop datanode/name-node setup .sh (done)
    - spark datanode/name-node setup .sh (in-progress)
    
2. Production System:
    1 - UI/UX (done)
    1 - Flask web (done)

3. Analytics System 
    - setup hadoop (done)
    - setup spark (in progress)
    - correlation task (not yet)


API
1# domain/signup [GET, POST] -> Sign up
1# /login [GET,POST] -> Login

0.5# /home [GET] -> Home page, display top rated books
# /book [GET, POST] -> Add a book -{asin,author,price .. }, search/get a book {asin,tile}

# /review [GET, POST] -> Retrieve review,  post a review

# For HTTP GET method -> parameters are passed via variables in URL, should not have body for GET
# POST -> Data is passed using Form Obj in flask 


##Questions for Profs:

Image instances: fixed? provided in "project" page

# Analytics-system 
image-ami ? 
This system consists of a cluster of servers? one name node + N data node?
Loading data from the production system, and store in a distributed file system?
what data should be loaded?
Scaling up and down => after Analytics-system is set up, can still add/delete nodes?
linux-user ubuntu instead of hadoop ?
ip instead of domain 

set up process:
1. set up data nodes, and a name node. assign public key to data node. 
2. configure private ips of data nodes to 'worker' in name node.
# To be done 
4. install sparks on each node
5. 3. start hadoop .sh / spark .sh in name node.

MASTER=private of name-node, WORKERS=private ips of data nodes?
hadoop 50070 port?
Zeppelin ?

both production/analytics system will set up/ turn off at the time?
