# coding: utf-8
from django.db import models

class Image(models.Model):
    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'Изображения'

    id       = models.BigIntegerField(u'ID', primary_key=True)
    text  = models.TextField(u'Описание', max_length = 10000, blank = True)
    width = models.BigIntegerField(u'Ширина', blank = True)
    height= models.BigIntegerField(u'Высота', blank = True)
    ext   = models.CharField(u'Расширение', blank = True, max_length = 5)

    def __unicode__(self):
        return str(self.id)

    def get_html(self):
        return '\n\
<div class=image>\
    <img src=/static/images/' + str(self.id) + '.jpg alt="' + self.text + '"/>\
</div>'
    #<div class=image_text>' + self.text + '</div>\

class Audio(models.Model):
    class Meta:
        verbose_name = 'аудиозапись'
        verbose_name_plural = 'Аудиозаписи'

    id       = models.BigIntegerField(u'ID', primary_key=True)
    artist   = models.CharField(u'Исполнитель', max_length = 1000)
    title    = models.CharField(u'Название', max_length = 1000)
    duration = models.BigIntegerField(u'Длительность')
    radio    = models.BooleanField(u'Радио', default = True)
    link     = models.CharField(u'Ссылка', max_length = 1000, blank = True)

    def __unicode__(self):
        return self.artist + ' - ' + self.title

    def get_duration(self):
        m = self.duration / 60;
        s = self.duration % 60;

        s = str(s) if s > 9 else '0' + str(s)
        return str(m) + ':' + str(s)

    def get_html(self):
        return '\n\
<div class=audio>\
    <div class=audio_info>%s - %s</div>\n\
</div>' % (self.artist, self.title)
'''
</div>' % (self.artist, self.title, self.id)
    <audio preload="none">\n\
        <source src="/static/music/%d.mp3" type="audio/mpeg">\n\
    </audio>\n\
    <object data="/static/player.swf" type="application/x-shockwave-flash" width=240 height=18>\n\
        <param value="/static/player.swf" name="movie">\n\
        <param value="loop=no&amp;autostart=no&amp;soundfile=/static/music/'+str(self.id)+'.mp3&amp;" name="flashvars">\n\
        <param value="false" name="menu">\n\
    </object>\n\
'''

class Video(models.Model):
    class Meta:
        verbose_name = 'видеозапись'
        verbose_name_plural = 'Видеозаписи'
    id       = models.BigIntegerField(u'ID', primary_key=True)
    oid      = models.BigIntegerField(u'Owner ID')
    title    = models.CharField(u'Название', max_length = 1000)
    descr    = models.TextField(u'Описание', max_length = 10000, blank = True)
    player   = models.CharField(u'Ссылка на плеер', max_length = 1000, blank = True)

    def __unicode__(self):
        return self.title

    def get_html(self):
        return '\n\
<div class=video>\n\
    <noindex>\n\
        <iframe src="%s" width="640" height="480" frameborder="0" allowfullscreen></iframe>\n\
    </noindex>\n\
    <div class=video_title>%s</div>\n\
    <div class=video_descr>%s</div>\n\
</div>' % (self.player, self.title, self.descr)
    #<iframe src="http://vk.com/video_ext.php?oid='+self.oid+'&id='+self.id+'&hash='+self.aid+'&hd=1" width="607" height="360" frameborder="0"></iframe>\n\

#class TagManager(models.Manager):
#    def get_query_set(self):
#        return super(TagManager, self).get_query_set().annotate(pubcount = models.Count('post__tags')).order_by('-pubcount', 'name')
#
class Tag(models.Model):
    #objects = TagManager()

    class Meta:
        verbose_name = 'ярлык'
        verbose_name_plural = 'Ярлыки'
        ordering = ['name']

    #id    = models.BigIntegerField(u'ID', primary_key=True)
#    id    = models.CharField(u'Имя', max_length = 100, primary_key = True)
    name  = models.CharField(u'Имя', max_length = 100)
    slug  = models.CharField(u'SLUG', max_length = 100, null = True, unique = True)
    public= models.BooleanField(u'Публичный', default = False)
    descr = models.TextField(u'Описание', max_length = 10000, blank = True)

    def __unicode__(self):
        return self.name

    def get_url(self):
        if self.slug is None:
            return str(self.id)
        return self.slug

class Ads(models.Model):
    class Meta:
        verbose_name = 'реклама'
        verbose_name_plural = 'Рекламные материалы'

    name    = models.CharField(u'Имя', max_length = 100)
    content = models.TextField(u'Содержание', max_length = 10000, blank = True)
    deleted = models.BooleanField(u'Удалено', default = False)
    public  = models.BooleanField(u'Публичный', default = False)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-datetime']

    id          = models.BigIntegerField(u'ID', primary_key=True)

    title       = models.CharField(u'Заголовок', max_length = 1000, blank = True, null = True)
    datetime    = models.DateTimeField(u'Дата публикации')
    content     = models.TextField(u'Содержание', max_length = 10000, blank = True)
    deleted     = models.BooleanField(u'Удалено', default = False)
    slug        = models.CharField(u'Адрес URL', max_length = 255, blank = True, null = True)

    showAds     = models.BooleanField(u'Показывать рекламу', default = False)

    ads         = models.ManyToManyField(Ads, blank = True)

    images      = models.ManyToManyField(Image, blank = True)
    audios      = models.ManyToManyField(Audio, blank = True)
    videos      = models.ManyToManyField(Video, blank = True)

    tags        = models.ManyToManyField(Tag, blank = True)

    def __unicode__(self):
        return str(self.id) + ' ' + self.content[:100]

    def get_absolute_url(self):
#        if self.slug is None:
#            return "/%i" % self.id
#
        return "/%i" % self.id

