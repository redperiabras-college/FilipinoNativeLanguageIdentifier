function loadFileAsText()
        {
            var fileToLoad = document.getElementById("select_file").files[0];

            var fileReader = new FileReader();
            fileReader.onload = function(fileLoadedEvent)
            {
                var textFromFileLoaded = fileLoadedEvent.target.result;
                document.getElementById("file_content").value = textFromFileLoaded;
            };

            try{
                 fileReader.readAsText(fileToLoad, "UTF-8");
            }
            catch(err){
                alert("Please choose some file...")
            }
        }

        $("#process").submit(function(event){

            // Prevent default posting of form - put here to work in case of errors
            event.preventDefault();

            // setup some local variables
            var $form = $(this);

            // Let's select and cache all the fields
            var $inputs = $form.find("textarea");

            // Serialize the data in the form
            var serializedData = $form.serialize();

            // Let's disable the inputs for the duration of the Ajax request.
            // Note: we disable elements AFTER the form data has been serialized.
            // Disabled form elements will not be serialized.
            $inputs.prop("disabled", true);

            // Fire off the request to /form.php
            request = $.ajax({
                url: "/",
                type: "post",
                data: serializedData
            });

            // Callback handler that will be called on success
            request.done(function (response, textStatus, jqXHR){
                // Log a message to the console
                $('#identification').text(response);
                $('#details').text('Given text is identified as '+response)
                $(".modal").modal('show');
            });

            // Callback handler that will be called on failure
            request.fail(function (jqXHR, textStatus, errorThrown){
                // Log the error to the console
                console.error(
                    "The following error occurred: "+
                    textStatus, errorThrown
                );
            });

            // Callback handler that will be called regardless
            // if the request failed or succeeded
            request.always(function () {
                // Reenable the inputs
                $inputs.prop("disabled", false);
            });

        });