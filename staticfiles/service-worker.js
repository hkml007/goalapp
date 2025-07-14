// service-worker.js

self.addEventListener('push', event => {
    const data = event.data.json();
    const { title, body, url } = data;
  
    const opts = {
      body,
      icon: '/static/img/reminder-icon.png', // Use your own icon path
      data: { url }
    };
  
    event.waitUntil(
      self.registration.showNotification(title, opts)
    );
  });
  
  self.addEventListener('notificationclick', ev => {
    ev.notification.close();
    ev.waitUntil(
      clients.openWindow(ev.notification.data.url || '/')
    );
  });
  