(function(){
  var b=document.querySelector('.menu-btn'),l=document.getElementById('nav-links');
  if(b&&l){b.addEventListener('click',function(){var o=l.classList.toggle('open');b.setAttribute('aria-expanded',o)});}
  var h=document.querySelector('.site-header');
  if(document.body.classList.contains('home')&&h){var f=function(){h.classList.toggle('scrolled',window.scrollY>40)};f();window.addEventListener('scroll',f,{passive:true});}
  var y=document.getElementById('year'); if(y) y.textContent=new Date().getFullYear();
  var qs=new URLSearchParams(location.search);
  document.querySelectorAll('form.lead-form').forEach(function(f){
    var t=qs.get('topic'),s=f.querySelector('#topic'); if(t&&s) s.value=t;
    var a=qs.get('address'),ai=f.querySelector('#address'); if(a&&ai) ai.value=a;
    f.addEventListener('submit',function(e){
      if(f.action.indexOf('YOUR_FORM_ID')===-1) return; // real Formspree endpoint configured
      e.preventDefault();
      var d=new FormData(f),body='';
      d.forEach(function(v,k){if(k.charAt(0)!=='_')body+=k+': '+v+'\n';});
      location.href='mailto:'+f.dataset.mailto+'?subject='+encodeURIComponent(f.dataset.subject||'Website inquiry')+'&body='+encodeURIComponent(body);
    });
  });
})();
