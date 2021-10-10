Vue.component('poem', {
    props: ['poem'],
    template: `
      <div class="poem">
        <div class="poem-text">
          {{poem.text}}
        </div>
        <button v-on:click='app.nextPoem(poem)'>Select</button>
      </div>
    `
  })
var app = new Vue({
    el: '#app',
    data: {
        incomplete: true,
        poem_pairs: [],
        poem_pair: [],
        chosen: [],
        poem_ix:-1,
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
            app.poem_pairs = responseObj.poem_pairs;
            app.poem_ix = 0;
            app.poem_pair = app.poem_pairs[app.poem_ix];
          };
        },
        nextPoem: function (poem) {
          app.chosen.push(poem.option);
          app.poem_ix++;
          if (app.poem_ix == app.poem_pairs.length){
            app.incomplete = false;
            app.poem_ix = -1;
          }
          else {
            app.poem_pair = app.poem_pairs[app.poem_ix];
          }
        },
    },
    created: function () {
      this.getPoems();
    },
})