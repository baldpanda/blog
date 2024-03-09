# Personal Blog

### Overview
Personal blog written using the [Flask web framework](https://flask.palletsprojects.com/en/3.0.x/). The ultimate goal of the application is to have a place to tinker with new tools including AI applications and also use as a forum for writing articles to try and work on communication skills


### Development

#### Conversational Agent Notes

Following a [Haytack tutorial](https://haystack.deepset.ai/tutorials/24_building_chat_app) for building a conversational agent and integrating it into the Flask application. Model being used for the conversational agent is `Zephyr 7B β`. Link on HuggingFace [here](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta). 

* Article on conversational agent's memory and how it is summarised [here](https://haystack.deepset.ai/blog/memory-conversational-agents)


#### Future Development Ideas

- **Deploy into AWS** - deploy app into AWS to make accessible over the internet. Could use EC2 instance or some form of containerised environment

- **Running coach** - sometimes the agent asks its own questions. Could do with some refinement

- **Front-end** - bit clumsy currently. Could be nice to make homepage a bit cleaner 

- **Testing** - quite light on testing currently. Good to add in some more testing. Maybe good to play around with some CI tools for doing things like checking coverage.

- **CI** - could test out `Ruff` for things like testing and linting. 

- **Technical notes** - good to add in some notes on the structure of the application.
