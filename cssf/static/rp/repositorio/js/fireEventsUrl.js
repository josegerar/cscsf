history.pushState = ( f => function pushState(){
    var ret = f.apply(this, arguments);
    window.dispatchEvent(new Event('pushstate'));
    window.dispatchEvent(new CustomEvent('locationchange', {data: arguments['0']}));
    return ret;
})(history.pushState);

history.replaceState = ( f => function replaceState(){
    var ret = f.apply(this, arguments);
    window.dispatchEvent(new Event('replacestate'));
    window.dispatchEvent(new CustomEvent('locationchange', {data: arguments['0']}));
    return ret;
})(history.replaceState);

window.addEventListener('popstate',(evt)=>{
    window.dispatchEvent(new CustomEvent('locationchange', {data: evt.state}));
});