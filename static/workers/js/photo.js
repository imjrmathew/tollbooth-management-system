(function () {
            var dataURL = '';
            var video = document.getElementById('video'),
                canvas = document.getElementById('canvas'),
                context = canvas.getContext('2d'),
                vendorUrl = window.URL || window.webkitURL;
            navigator.getMedia = navigator.getUserMedia ||
                                 navigator.webkitGetUserMedia ||
                                 navigator.mozGetUserMedia ||
                                 navigator.msGetUserMedia;
            navigator.getMedia({
                video: true,
                audio: false
            }, function (stream) {
                    video.srcObject = stream;
                    video.play();
            }, function (error) {

            });
            var button = document.getElementById('capture');
            document.getElementById('capture').addEventListener('click', function () {
                context.drawImage(video, 0, 0, 470,  370);
                dataURL = canvas.toDataURL('image/png');
                Pic = dataURL;
                $("#value").val(Pic);
                $.ajax({
                    type: "POST",
                    url: "/Workers/SaveImage/",
                    data: '{ "imageData" : "' + Pic + '" }',
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    success:function(data){
                        document.getElementById("myhead").innerHTML = data['msg'];
                    }
                });
            })
    })();