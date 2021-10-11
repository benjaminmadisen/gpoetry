Vue.component('poem', {
    props: ['poem'],
    template: `
      <div v-if='app.incomplete' tabindex="0" class="poem clickable" v-on:click='app.nextPoem(poem)'>
        <pre class="poem-text clickable">
          {{poem.text}}
        </pre>
      </div>
      <div v-else class="poem review" v-bind:class="{chosen: poem.chosen, correct: poem.type=='real'}">
        <pre class="poem-text review">
          {{poem.text}}
        </pre>
      </div>
    `
  })
var app = new Vue({
    el: '#app',
    data: {
        incomplete: true,
        review: false,
        poem_pairs: [],
        poem_pair: [],
        correct: 0,
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
            app.poem_ix = -1;
            app.incomplete = true;
            app.review = false;
            app.correct = 0;
          };
        },
        begin: function () {
          app.poem_ix = 0;
          app.poem_pair = app.poem_pairs[app.poem_ix];
        },
        nextPoem: function (poem) {
          app.poem_ix++;
          if (app.poem_ix == app.poem_pairs.length){
            app.incomplete = false;
            app.poem_ix = -1;
          }
          else {
            app.poem_pair = app.poem_pairs[app.poem_ix];
          }
          if (poem != -1){
            poem.chosen = true;
            if (poem.type === "real"){app.correct++}
            
          }
        },
        prevPoem: function () {
          app.poem_ix--;
          app.poem_pair = app.poem_pairs[app.poem_ix];
        },
        reviewPicks: function () {
          app.poem_ix = 0;
          app.poem_pair = app.poem_pairs[app.poem_ix];
          app.review = true;
        },
    },
    created: function () {
      this.getPoems();
    },
})