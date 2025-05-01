# Intelligent-Resume-Parser using SharpAPI 
This resume parser is built using sharpAPI's API key. The first step, would be to install/import necessary libraries like OS, dotenv, JSON, sharpAPI. Then we load the variables in a dot env file. Initialize the sharpAPI service with your API key. Add the resume link to the file path given. Then, you'll get an output of parsed resume data which will be in the form of string. To convert the string form of output into JSON form we have few more steps to follow. First, get the raw string data and parse it once to get proper JSON string form of output. Second in order to parse the output received and convert it into python dict format we are parsing the output again. Finally, we are dumping the data in json to get a proper JSON form of output. 
###Libraries/Tools Used
###1.OS - It is a standard python library, that interacts with the operating system (eg: accessing environment variables, file paths)
###2.DOTENV - It is one of the 3rd party python libraries that loads environment variables from a .env file into os.environ.
###3.JSON - It is a standard python library that Parses JSON strings/files and converts Python objects to JSON.
###4.sharpAPI - SharpAPI Python Client SDK enables developers to integrate advanced artificial intelligence capabilities into their Python applications. This SDK simplifies interaction with the SharpAPI services, providing a seamless way to leverage AI for various use cases. 
###Assumptions/ Limitations
Language/Format Support - Likely optimized for English; may not support all languages or scanned images.
Rate limits / Quotas - API calls may be rate-limited based on your subscription.
Black-box - Internals of parsing (rules vs ML) may not be visible or customizable.
