# Dockerfile for defi project
#
# Create a user called birdman
# Set up an environment under this user
#
# Use the continuum io image for minoconda
FROM continuumio/miniconda3

RUN apt-get update -y --fix-missing
RUN apt-get install -y vim curl pkg-config gcc
RUN apt-get -y install sudo

# Probably not needed with the conda image.
# Make sure conda is in the path for root, and in the default bash profile
ENV PATH=/opt/conda/bin:$PATH
ENV PATH=/opt/conda/envs/app/bin:$PATH
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile

# Create a non-root user to run the app
# The conda environment with everything beyond the basics
# will be built in this user's home 
ENV USER birdman
ENV UID 1002
ENV GID 1003
ENV HOME /home/$USER
RUN addgroup --gid $GID traders
RUN adduser --disabled-password \
    --gecos "Non-root user" \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    $USER

#RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN adduser birdman sudo

# This user now owns conda. This might be overkill
RUN chown $UID:$GID /opt/conda

# Make a data directory to hold things we want to persist
# or so that the host can communicate. This is paried
# with a volume mount in the entrypoint script.
VOLUME /home/$USER/data
RUN chown $UID:$GID /home/$USER/data/

# Set up the users home as a working directory
ENV WORKDIR /home/$USER/app
WORKDIR $WORKDIR
VOLUME $WORKDIR
ENV PATH=$WORKDIR:$PATH
RUN chown $UID:$GID $WORKDIR

# Entrypoint to the user's root home
# Having it in the working directory creates problems
# with files being changed back and forth.
COPY --chown=$UID:$GID entrypoint.sh /home/$USER
RUN chmod +x /home/$USER/entrypoint.sh

# Get the conda environment file and give it to the user 
COPY --chown=$UID:$GID web3_environment.yml /tmp/environment.yml
# Switch to the non-root user to build conda environment
# The order here is really important
# Create an env as the user in the default localtion.
USER $USER
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
RUN conda init bash
RUN conda env create --file /tmp/environment.yml --name app
RUN conda update --name app --channel defaults conda
RUN conda clean --all --yes
RUN conda config --prepend pkgs_dirs /home/birdman/.conda/pkgs

# Export env file here for reproduction (before manual installations)
# When the conda environment install doesn't work, use this pattern to build manually.
# Careful then of exporting the environment with this in it.
SHELL ["/bin/bash", "--login", "-c"]
#RUN conda activate /home/birdman/.conda/envs/app && \
#    conda install --prefix /home/birdman/.conda/envs/app -c conda-forge ta-lib && \
#    conda deactivate

RUN echo "conda activate app"  >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Setup entry files and app script
# EXPOSE 5001
ENTRYPOINT ["/home/birdman/entrypoint.sh"]
#CMD [ "/bin/bash" ]

