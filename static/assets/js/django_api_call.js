$('#id_city_id').select2();
    // calling api on button click
    $(document).ready(function() {
        
        $('#search-now').click(function(e) {

            e.preventDefault(); 

            // Get selected city value
            var selectedCity = $('#id_city_id').val();

            // Make AJAX call to the Django view
            $.ajax({
                type: 'POST',
                url: '/get_weather_info/',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    city_id: selectedCity
                },
                success: function(response) {
                    console.log(response)
                    if(response.data.status === "success"){
                    $('.weather-info').html(
                            '<p>City : <strong>' + response.data.city + '</strong></p>' +
                            '<p>Temperature: <strong>' + response.data.temp + '</strong></p>' +
                            '<p>Humidity: <strong>' + response.data.humidity + '</strong></p>' +
                            '<p>Visibility: <strong>' + response.data.visibility + '</strong></p>' +
                            '<p>Dew Point: <strong>' + response.data.dew_point + '</strong></p>' +
                            '<p>Pressure: <strong>' + response.data.pressure + '</strong></p>' +
                            '<p>UV Index: <strong>' + response.data.uv_index + '</strong></p>'
                        );

                    }
                    else{
                      alert(response.data)
                    }
                },
                error: function(xhr, status, error) {
                    alert("somthing went wrong! cotact admin")
                }
            });
        });
    });