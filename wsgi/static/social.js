// Twitter JS
function update_twitter() {
    !function(d,s,id){
        console.debug(d)
        console.debug(s)
        console.debug(id)
        var js,
            fjs = d.getElementsByTagName(s)[0],
            p=/^http:/.test(d.location)?'http':'https';
        if(!d.getElementById(id)){
            js=d.createElement(s);
            js.id=id;
            js.src=p+'://platform.twitter.com/widgets.js';
            fjs.parentNode.insertBefore(js,fjs);
        }
    } (document, 'script', 'twitter-wjs');
    twttr.widgets.load();
}
function update_vk(id, title, content, pid) {
    if (title == null) title = 'Мишка Механический';
    if (title == "None") title = 'Мишка Механический';
    /*
    console.debug(id);
    console.debug(title);
    console.debug(content);
    console.debug(pid);
    */

    image = "http://www.MechanicalBear.ru/static/bear.jpg";
    if (pid > 0)
        image = "http://www.MechanicalBear.ru/static/images/" + pid + ".jpg";
        
    VK.Widgets.Like('vk_like_' + id, {
        type: "mini",
        pageTitle: title,
        pageDescription: content,
        pageUrl: "http://www.MechanicalBear.ru/" + id,
        pageImage: image,
    }, id);
}
function update_vk_list(data) {
    data.forEach(function(item){
        pid = item.fields.images;
        if (pid.length) pid = pid[0].pk;
        else pid = 0;

        update_vk(item.pk, item.fields.title, item.fields.content, pid);
    });
}
