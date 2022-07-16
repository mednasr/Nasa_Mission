# NASA web Scraping

## Project Goal
 - Create a small open to the world instance in a free AWS account, or use your own if you have one.
 - On that server, build a website that first you’ll be promoted to a login page where you need to put valid credentials.
 - Behind it, there will be a small backend that will do some site scraping to pull whatever information you like, it can a retailer site, second hand site, your own data from a different site you might own, it doesn't matter as long as it's being pulled from somewhere.
 - On the web page, present the information you pulled in a table.
 - Provide the option to download the table as an Excel sheet.
 - Be able to consume the same info using an API.
 - The languages you'll be using are your choice.

   - ### AWS EC2 instance configuration steps:
     #### Installation and configuration of Selenium Grid  using SeleniumHQ Docker Images 
     - Connect tou the EC2 instance with Putty ( you can login in to the instance using ip :  ec2-52-55-160-227.compute-1.amazonaws.com and the attached key : mars_key.ppk and user : ubuntu )
     - Install Docker on the AWS instance: sudo yum install -y docker
     - Start the docker service: sudo service docker start
     - Add the ubuntu to the Docker group: sudo usermod -a -G docker ec2-user
     - Close the Terminal and connect again with SSH to reset permissions.
     - Run docker info to see that docker is well installed
     #### For our installation, the Docker images we will be using:
     - selenium/hub: Image for running a Grid Hub. It will expose port 4444 on the AWS instance so we can connect to the Selenium Grid.
     - selenium/node-chrome: Grid Node with Chrome installed, needs to be connected to a Grid Hub
     - selenium/node-firefox: Grid Node with Firefox installed, needs to be connected to a Grid Hub
     #### According to Selenium HQ's instructions, you need to create a Docker Network.
     - First, we need to install Compose (Check official documentations for more details https://docs.docker.com/compose/install/) by running this command :
     - sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 
     - apply executable permissions :
     - sudo chmod +x /usr/local/bin/docker-compose
     - test the installation by running
     - docker-compose --version 
     - Create a “docker-compose.yml” (by running touch command)
     - Edit the file in the nano text editor by running: nano docker-compose.yml
     - Copy & paste the next content in the created file
     #### To execute this file, use docker-compose -f <file_name> up
     #### Add the "-d" flag at the end for detached execution   
     ```docker
     version: '2'   
     services:   
     firefox:   
     image: selenium/node-firefox:3.141.59-20210311 
     volumes:   
      - /dev/shm:/dev/shm   
     depends_on:   
      - hub   
     environment:   
      HUB_HOST: hub   
     chrome:   
     image: selenium/node-chrome:3.141.59-20210311 
     volumes:   
      - /dev/shm:/dev/shm   
     depends_on:   
      - hub   
     environment:   
      HUB_HOST: hub   
     hub:   
     image: selenium/hub:3.141.59-20210311 
     ports:   
      - "4444:4444"

   - Save the file and Exit. To check the file content, run : cat docker-compose.yml
   - Now you can start and stop the containers using the commands : 
   - docker-compose up -d
   - docker-compose down

  ### Deploy our Python API 

   - Install python and pip  on the current machine
   - sudo yum update
   - sudo yum install python3
   - sudo yum install epel-release
   - sudo yum install python-pip

   - Also install git and add ssh key
   - sudo yum install git
   - create gitlab ssh key to be able to clone your project 
   - Now we need to clone the API repository into your home directory 
   - git clone git@gitlab.com:mohamed.nasr/nasa-news.git

   - Using pip, install virtualenv
   - sudo pip install virtualenv
   - create & setup a virtual environment inside the project folder 
   - virtualenv venv
   - activate your virtual environment
   - source ./venv/bin/activate

   - We need to install the requirements of the project by running
   - pip install -r requirements.txt 

   - Also, install gunicorn in the active “venv”
   - pip install gunicorn

   - Make sure to check that the port you are using is allowed in the security group of your instance (check inbound rules)
   - Test one of the API links using Postman, to make sure that it’s running 

   - Now will create a WSGI file wsgi.py it does not exist in the repository already) to bind the application to Gunicorn
        ```wsgi
        from app import app 
        if __name__ == "__main__":
            app.run() 

   - Run the next command to start the app (-D/--daemon option to daemonize the Gunicorn the process), and specifiy the file name (:app) otherwise WSGI will put application as default :
   - gunicorn --bind 0.0.0.0:8080 -D wsgi:app
   - Now the process will keep on running in the background



 - ### Initial scraping using BeautifulSoup, Pandas, and Requests/Splinter.
   - Setup splinter
   - Scraping using **BeautifulSoup** based on the inspected **html tag**
   ```python
    nasa_products = []
    for product in products:
        # Error handling
        try:
            # Extract href
            href = product.a['href']
            browser.visit(href)
            html = browser.html
            soup = bs(html, 'html.parser')

            product_title = soup.find('h1').text
            product_desc = soup.find('div', class_="text").li.text
            product_img = soup.find('img', class_="feature-image")['src']

            nasa_dict = {
                "product_src": product_img,
                "product_title": product_title,
                "product_desc": product_desc
            }
            nasa_products.append(nasa_dict)

        except Exception as e:
          print(e)
   ```
   - Using Pandas **read_html** to scaping the website and store the information into a DataFrame. Generating html table using **to_html** function
   ```python
     facts_url = 'https://galaxyfacts-mars.com/'
     tables = pd.read_html(facts_url)

     # generate HTML tables from DataFrames
     html_table = fact_df.to_html()
     html_table.replace('\n', '')
   ```
 - #### Use MongoDB with Flask templating to  save the scrapped data and to create a new HTML page that displays all the information that was scraped from the URLs above if needed.
   - Create an ES2 t2.micro instance to host thje application on it 
   - Run a Docker containers on the AWS EC2 to be able to quickly deploy and scale your application into any environment.
   - Install Gunicorn HTTP server to run concurrently multiple Python processes within a single dyno.
   - Create a route "/scrape" that will import Python script .
   - Create a route "/" that will redirect you to a login page ( username : admin , psw : admin ).
   - Create a root route "/home" that will import Python script to scrape the needed data and display it, or you can query Mongo database and pass the nasa data into an HTML template to display the data.
   - Create a route "/get_all_data" to get all data scrapped using the get request.
   - Create a template HTML file called index.html that will take the nasa data dictionary and display all the data in the appropriate HTML elements.
   - Create a template HTML file called login.html that will give you the possibility to login into the scraper.
 
 - #### Final Results
   - Test the website by visiting : http://52.55.160.227:8000/
 - ### Run the project locally
 - Clone the project into your local machine 
 - Install all dependencies ( can be found in requirements.txt and can be automated if you use an IDE like Pycharm )
 - Run : 
   - python app.py 
 - the app should be running, and you can check it by navigating to : http://127.0.0.1:5000/


