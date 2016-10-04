# GA4GH API Example: gemini database

Here is an example of adopting the GA4GH API to an existing and external project: the Gemini software framework for exploring genome variation.

## Prerequisites

We'll use the Protocol Buffer compiler utility to compile the schema definitions.  Please see [these](https://github.com/ga4gh/schemas/blob/master/doc/source/appendix/swagger.rst#installing-prerequisites) instructions to make sure that the `protoc` command is available on your system.

We'll use *swagger-codegen* to create our template Python-based server code; just being able to execute its jar file will suffice.  Here's some commands to create the jar file:

```
git clone https://github.com/swagger-api/swagger-codegen.git
cd swagger-codegen
mvn clean package
# java -jar ./modules/swagger-codegen-cli/target/swagger-codegen-cli.jar help
```

## Instructions

First, we have to take the schemas [the \*.proto files in the 'schemas' repository], and produce swagger API definitions [\*.swagger.json files] from them, via the `protoc` utility.

```
git clone https://github.com/ga4gh/schemas.git
cd schemas
mkdir -p target/swagger
```

Since the swagger-codegen.jar command line utility only accepts 1 API definition file as input, our services will need to all be defined in one file.  Currently, in the schemas repository, they are defined as [many files](https://github.com/ga4gh/schemas/tree/master/src/main/proto/ga4gh).  I've manually combined them all in to 1 file called *all_services.proto*.  Let's copy that file to the same location as the others:

```
cp path/to/all_services.proto ./src/main/proto/ga4gh
```

Now we use the `protoc` utility:

```
protoc -I./src/main/proto --swagger_out=. src/main/proto/ga4gh/all_service.proto
```

This should produce a directory 'ga4gh', and inside it, all_service.swagger.json ; this is the swagger API service definition file.


Now we use the all_service.swagger.json swagger file from step 1 to produce stub server code, via the _swagger-codegen.jar_ utility.

To support Python 2 in the output stub server, create a JSON configuration file with {"supportPython2":"True"} in it.  Pass this file to swagger-codegen-cli's 'generate' command, via the -c option; we'll call it temp.json .

```
java -jar swagger-codegen.jar generate -i schemas/target/swagger/ga4gh/all_service.swagger.json -l python-flask -o /tmp/server -c temp.json
```

The folder "server" should then be a Python flask-based stub server that one needs to modify.  You need to make it so that the server implements the GA4GH interface, and calls the Gemini database in the background.

Rename all of the modules in server/controllers/* so that they go from like_this_controller.py to LikeThis_controller.py .  The reason this step is needed, is because, for some reason, the generated server code expects the modules to look like that, and I don't know how to make it expect otherwise, so this is a workaround.

```
mv server/controllers/read_service_controller.py server/controllers/ReadService_controller.py
```

Also, go inside each one of those files and change the paramaters to each function from CamelCase to underscore_case.  The server will fail to start without performing this step.  So for example, if inside one of the files you have a definition like "def my_function(datasetId):", change it to "def my_function(dataset_id):".

Now we load an example VCF file into the gemini SQLite database:

```
gemini load -v file.vcf my.db
```

Start the server with:

```
python server/app.py
```

Navigate to http://localhost:8080/ui/

Edit the files under 'controllers' in your stub server.  Their names may need to be modified from something_like_this_controller.py to SomethingLikeThis_controller.py .  Inside each file though, you may have to change variable names from CamelCase to under_score_case
