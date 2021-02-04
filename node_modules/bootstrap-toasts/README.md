## bootstrap-toasts

**Beta time**

Bootstrap components <a href="https://getbootstrap.com/docs/4.3/components/toasts/" title="Toasts">"Toasts"</a>

Currently relying on Bootstrap and jQuery environments, because it is a function extension of Bootstrap.

Supports arbitrary calls of ten parameters, supports callback functions based on toasts events.


<p align="center">
<img alt="GitHub Release" src="https://img.shields.io/github/release/zhangchenglin/bootstrap-toasts.svg">
<img alt="GitHub License" src="https://img.shields.io/github/license/zhangchenglin/bootstrap-toasts.svg">
</p>
<p align="center">
<a href="https://www.npmjs.com/package/bootstrap-toasts" target="_blank"><img alt="NPM Version" title="NPM Package" src="https://img.shields.io/npm/v/bootstrap-toasts.svg"></a>
<img alt="NPM License" src="https://img.shields.io/npm/l/bootstrap-toasts.svg">
</p>
<p align="center">
<a href="https://www.jsdelivr.com/package/npm/bootstrap-toasts" target="_blank"><img src="https://data.jsdelivr.com/v1/package/npm/bootstrap-toasts/badge?style=rounded" alt="jsDelivr" title="jsDelivr"></a>
</p>

## Demo 

<a href="https://zhangchenglin.github.io/bootstrap-toasts/demo.html" target="_blank" title="bootstrap-toasts DEMO">https://zhangchenglin.github.io/bootstrap-toasts/demo.html</a>


## How to install?
```
npm install bootstrap-toasts --save
```

## CDN
- **jsDelivr**
```
<script src="https://cdn.jsdelivr.net/npm/bootstrap-toasts/dist/bootstrap-toasts.js"></script>
```
```
<script src="https://cdn.jsdelivr.net/npm/bootstrap-toasts/dist/bootstrap-toasts.min.js"></script>
```

## How to use it?
```
<script src="/bootstrap-toasts.min.js"></script>

bootstrapToasts(title, content, titleColor, delay, position, releaseTime, icon, eventType, eventFunction, ariaType)
```


## Parameter Description

- **title**

Type:String

Default value:undefined

Description:

---
- **content**

Type:String

Default value:undefined

Description:

---
- **titleColor**

Type:String

Default value:

Description:

| parameter|
| :-------:| 
| primary  |
| secondary|
| success  |
| danger   |
| warning  |
| info     |
| dark     |

---
- **delay**

Type:Number

Default value:10

Unit:second

Description:

min value: 1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  max value: any

| parameter | similar code |
| :-------: | :---------- |
| 1         |  ```<div class="toast" data-delay="1000"></div>``` |
| 2         |  ```<div class="toast" data-delay="2000"></div>``` |
| 3         |  ```<div class="toast" data-delay="3000"></div>``` |
| ...       |  ```...``` |

---
- **position**

Type:String

Default value:

Description:

| parameter     |
| :-----------: |
| topLeft       |
| topCenter     |
| topRight      |
| bottomLeft    |
| bottomCenter  |
| bottomRight   |
| center        |

---
- **releaseTime**

Type:String

Default value:

Description:

---
- **icon**

Type:String

Default value:undefined

Description:

| parameter |
| :-------: |
| success   |
| danger    |
| warning   |
| info      |

- **eventType**

Type:String

Default value:undefined

Description:

eventType and eventFunction must exist at the same time, otherwise the event function will be invalid.

| parameter |
| :-------: |
| show      |
| shown     |
| hide      |
| hidden    |

- **eventFunction**

Type:Function

Default value:undefined

Description:

eventType and eventFunction must exist at the same time, otherwise the event function will be invalid.

- **ariaType**

Type:String

Default value:alert

Description:

| parameter |
| :-------: |
| alert     |
| status    |

