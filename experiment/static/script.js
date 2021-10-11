Vue.component('poem', {
    props: ['poem'],
    template: `
      <div class="poem display" v-if='app.incomplete' tabindex="0" class="poem clickable" v-on:click='app.nextPoem(poem)'>
        <div class="poem-title">
          {{poem.name}}
        </div>
        <pre class="poem-text clickable">
          {{poem.text}}
        </pre>
      </div>
      <div v-else class="poem review" v-bind:class="{chosen: poem.chosen, correct: poem.type=='real'}">
        <div class="poem-title">
          {{poem.name}}
        </div>
        <div v-if="poem.type=='real'" class="poem-author">
          by {{poem.author}}
        </div>
        <div v-else class="poem-author">
          by GPT3 pretending to be {{poem.author}}
        </div>
        <pre class="poem-text review">
          {{poem.text}}
        </pre>
      </div>
    `
  })
  Vue.component('poem-result', {
    props: ['poem_pair'],
    template: `
      <tr class="poem-result" v-on:click='app.reviewPoem(poem_pair[0].ix-1)'
                               v-bind:class="{result_correct: (poem_pair[0].type=='real' && poem_pair[0].chosen) ||
                                                              (poem_pair[0].type=='fake' && !poem_pair[0].chosen)}">
        <td class="poem-ix"> {{poem_pair[0].ix}} </td>
        <td class="poem-result-title first" v-bind:class="{result_chosen: poem_pair[0].chosen, result_correct: poem_pair[0].type=='real'}"> {{poem_pair[0].name}} </td>
        <td class="poem-result-title second" v-bind:class="{result_chosen: poem_pair[1].chosen, result_correct: poem_pair[1].type=='real'}"> {{poem_pair[1].name}} </td>
          
      </tr>
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
        reviewPoem: function (ix) {
          app.poem_ix = ix;
          app.poem_pair = app.poem_pairs[app.poem_ix];
          app.review = true;
        },
    },
    created: function () {
      this.getPoems();
    },
})