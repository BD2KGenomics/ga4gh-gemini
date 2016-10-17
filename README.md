# GA4GH API Example: Gemini database

Here is an example of adopting the GA4GH API to an existing and external project: the [Gemini](https://github.com/arq5x/gemini) software framework for exploring genome variation.

## Prerequisites

We'll use the Protocol Buffer compiler utility to compile the schema definitions.  Please see [these](https://github.com/ga4gh/schemas/blob/master/doc/source/appendix/swagger.rst#installing-prerequisites) instructions to make sure that the `protoc` command is available on your system.

We'll use *swagger-codegen* to create our template Python-based server code; just being able to execute its jar file will suffice.  Here's some commands to create the jar file:

```
git clone https://github.com/swagger-api/swagger-codegen.git
cd swagger-codegen
mvn clean package
# java -jar ./modules/swagger-codegen-cli/target/swagger-codegen-cli.jar help
# Or..
# wget http://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.1/swagger-codegen-cli-2.2.1.jar -O swagger-codegen-cli.jar
# java -jar swagger-codegen-cli.jar help
```

## Instructions

First, we have to take the schemas [the \*.proto files in the 'schemas' repository], and produce swagger API definitions [\*.swagger.json files] from them, via the `protoc` utility.

```
cd ..
git clone https://github.com/ga4gh/schemas.git
cd schemas
mkdir -p target/swagger
```

Since the swagger-codegen.jar command line utility only accepts 1 API definition file as input, our services will need to all be defined in one file.  Currently, in the schemas repository, they are defined as [many files](https://github.com/ga4gh/schemas/tree/master/src/main/proto/ga4gh).  I've manually combined them all in to 1 file called [*all_services.proto*](https://github.com/BD2KGenomics/ga4gh-gemini/blob/master/all_service.proto).  Let's copy that file to the same location as the others:

```
cp path/to/all_services.proto ./src/main/proto/ga4gh
```

Now we use the `protoc` utility; the output directory will be the current directory, and the input file will be that all_services.proto file:

```
protoc -I./src/main/proto --swagger_out=. src/main/proto/ga4gh/all_services.proto
# If you wanted to process more than one *.proto file, you can do
# protoc -I./src/main/proto --swagger_out=. src/main/proto/ga4gh/*service.proto
```

This should produce a directory 'ga4gh', and inside it, all_services.swagger.json ; this is the swagger API service definition file.


Now we use the all_services.swagger.json swagger file to produce stub server code, via the `swagger-codegen.jar` utility.

To support Python 2 in the output stub server, create a JSON configuration file with {"supportPython2":"True"} in it.  Pass this file to swagger-codegen-cli's 'generate' command, via the -c option; we'll call it temp.json.

```
java -jar swagger-codegen.jar generate\
  -i schemas/target/swagger/ga4gh/all_services.swagger.json\
  -l python-flask -o server -c temp.json
```

The folder "server" should then be a Python flask-based stub server that one needs to modify.  It needs to be made so that the server implements the GA4GH interface, and calls the Gemini database in the background.

Rename all of the modules in server/controllers/\* so that they go from *like_this_controller.py* to *LikeThis_controller.py*.  The reason this step is needed, is because, for some reason, the generated server code expects the modules to look like that, and I don't know how to make it (the swagger-codegen.jar utility) expect otherwise, so this is a workaround.

```
mv server/controllers/read_service_controller.py server/controllers/ReadService_controller.py
```

Also, go inside each one of those files and change the paramaters to each function from CamelCase to underscore_case.  The server will fail to start without performing this step.  So for example, if inside one of the files you have a definition like "def my_function(datasetId):", change it to "def my_function(dataset_id):".

Now we load an example VCF file into the gemini SQLite database:

```
wget https://github.com/ga4gh/server/releases/download/data/ga4gh-example-data_4.5.tar
tar xf ga4gh-example-data_4.5.tar
gemini load -v ga4gh-example-data/chr1.vcf.gz my.db
```

Start the server with:

```
python server/app.py
```

Navigate to http://localhost:8080/ui/ and you'll see your documentation for your api.
