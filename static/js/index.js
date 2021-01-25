if("serviceWorker" in navigator)
{
	navigator.serviceWorker.register("sw.js").then(registration =>
	{
		console.log("SW Registered!");
		console.log(registration);
	}).catch(error =>
	{
		console.log("SW Couldnt register!");
		console.log(error);
	})

	Notification.requestPermission(function(status) {
    console.log('Notification permission status:', status);

});

	function displayNotification() {
  if (Notification.permission == 'granted') {
    navigator.serviceWorker.getRegistration().then(function(reg) {
      var options = {
        vibrate: [100, 50, 100],
        data: {
          dateOfArrival: Date.now(),
          primaryKey: 1
        }
      };
      reg.showNotification('Hello world!', options);
    });
  }
}

displayNotification();


}