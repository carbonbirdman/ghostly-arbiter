A simple arbitrage script written in Python Web3 and wrapped in a Docker container for ease of deployment.

To run

1. build.sh

This creates a Docker image with conda installed. On the container it cretes a
user account to run the script as, sets up a few directories and then installs
some packages to conda using the web3_environment.yml file.

2. shell.sh

This creates an instance of the docker container and logs into it. From here you can run shell
commands in the container. 

3. conda activate app
4. ipython
5. %run arb_search.py

The run.sh script and entrypoint.sh are used when you want to run it on the container in the background.


List of dexes and tokens is set in script.

You will need to add a file called ftm_secrets.py with your account key and RPC url - be extremely careful with this file!

I can't guarantee the security of the Docker setup or the Python code: if you decide to run this connected to a real account,
please do your own research into security of running containers and don't use an account with your life savings!

Sleep statements may need adjusting if you find yourself over your request limit, depnding on your Ankr plan.

If this is useful to you I would appreciate knowing.

Tips: 0x1fd2181A7b6c21f9e54330EfFbd3EAbC88853FbF
