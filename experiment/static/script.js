Vue.component('poem', {
    props: ['poem'],
    template: `
      <div class="poem">
          {{poem.text}}
      </div>
    `
  })
var app = new Vue({
    el: '#app',
    data: {
        in_progress: false,
        poem_pair: [],
      },
      methods: {
        getPoems: function () {
          let xhr = new XMLHttpRequest();
          xhr.open('GET', '/get_poems');
          xhr.responseType = 'json';
          xhr.send();

          var app = this;
          xhr.onload = function() {
            let responseObj = xhr.response;
            app.poem_pair = responseObj.poem_pair;
            app.in_progress = true;
          };
        },
    }
})