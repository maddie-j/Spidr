
    var pictureSource;   // picture source
    var destinationType; // sets the format of returned value

    // Wait for device API libraries to load
    //
    document.addEventListener("deviceready",onDeviceReady,false);

    // device APIs are available
    //
    function onDeviceReady() {
        pictureSource=navigator.camera.PictureSourceType;
        destinationType=navigator.camera.DestinationType;
    }


    function onPhotoDataSuccess(imageData) {
      // Get image handle
      //
      var smallImage = document.getElementById('smallImage');

      // Unhide image elements
      //
      smallImage.style.display = 'block';

      smallImage.src = "data:image/jpeg;base64," + imageData;

      $.ajax({
        type:'POST',
        url: "http://10.1.1.108:5000/identify",
        data: {
          imageData: imageData
        }
      });

    }

    // Called when a photo is successfully retrieved
    //
    function onPhotoURISuccess(imageData) {

      // Get image handle
      //
      var largeImage = document.getElementById('largeImage');

      // Unhide image elements
      //
      largeImage.style.display = "data:image/jpeg;base64," + 'block';

      // Show the captured photo
      // The in-line CSS rules are used to resize the image
      //
      largeImage.src = imageData;

      $.ajax({
        type:'POST',
        url: "http://10.1.1.108:5000/identify",
        data: {
          imageData: imageData
        }
      });
    }

    // A button will call this function
    //
    function capturePhoto() {
      // Take picture using device camera and retrieve image as base64-encoded string
      navigator.camera.getPicture(onPhotoDataSuccess, onFail, { quality: 50,
        destinationType: destinationType.DATA_URL});
    }
    function getPhoto(source) {
      // Retrieve image file location from specified source
      navigator.camera.getPicture(onPhotoURISuccess, onFail, { quality: 50,
        destinationType: destinationType.DATA_URL,
        sourceType: source });
    }

    // Called if something bad happens.
    //
    function onFail(message) {
      if(message == "no image selected"){
        return;
      }
      alert('Failed because: ' + message);
    }
