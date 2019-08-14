function refresh(data_item){
  var id_time = data_item + "_time";
  var id_content = data_item + "_content";
  if(data_item == 'baidu_now' || data_item == 'baidu_today' || data_item == 'baidu_week' || data_item == 'tieba'){
    var id_time = "baidu_time";
    var id_content = "baidu_content";
  }
  if(data_item == 'zhihu_good' || data_item == 'zhihu_hot' || data_item == 'zhihu_daily'){
    var id_time = "zhihu_time";
    var id_content = "zhihu_content";
  }
  if(data_item == 'hacpai_play' || data_item == 'hacpai_hot'){
    var id_time = "hacpai_time";
    var id_content = "hacpai_content";
  }
  if(data_item == 'weixin_hot'){
    var id_time = "weixin_time";
    var id_content = "weixin_content";
  }
  if(data_item == 'smzdm_article_today' || data_item == 'smzdm_article_week' || data_item == 'smzdm_article_month'){
    var id_time = "smzdm_article_time";
    var id_content = "smzdm_article_content";
  }
  if(data_item == 'itunes_paid_cn' || data_item == 'itunes_free_cn' || data_item == 'itunes_revenue_cn'){
    var id_time = "itunes_cn_time";
    var id_content = "itunes_cn_content";
  }
  if(data_item == 'itunes_paid_us' || data_item == 'itunes_free_us' || data_item == 'itunes_revenue_us'){
    var id_time = "itunes_us_time";
    var id_content = "itunes_us_content";
  }
  if(data_item == 'toutiao_a' || data_item == 'toutiao_b' || data_item == 'toutiao_c' || data_item == 'toutiao_d' || data_item == 'toutiao_e'){
    var id_time = "toutiao_time";
    var id_content = "toutiao_content";
  }
  if(document.getElementById(id_time)){
    document.getElementById(id_time).innerHTML = '更新时间';
  }
  if(document.getElementById(id_content)){
    if(data_item != 'toutiao_b' && data_item != 'toutiao_c' && data_item != 'toutiao_d' && data_item != 'toutiao_e'){
      document.getElementById(id_content).innerHTML = "";
      var tag = "<p>更新中......</p>";
      document.getElementById(id_content).insertAdjacentHTML("beforeEnd",tag);
	}
  }
  html_xr(data_item);
  if(data_item == 'toutiao_a'){
    setTimeout("html_xr('toutiao_b')",1000);
    setTimeout("html_xr('toutiao_c')",1000);
    setTimeout("html_xr('toutiao_d')",1000);
    setTimeout("html_xr('toutiao_e')",1000);
    setTimeout("html_xr('toutiao_f')",1000);
    setTimeout("html_xr('toutiao_g')",1000);
    setTimeout("html_xr('toutiao_h')",1000);
    setTimeout("html_xr('toutiao_i')",1000);
    setTimeout("html_xr('toutiao_j')",1000);
  }
};

function html_xr(data_item){
  var now=new Date();
  var number = now.getYear().toString()+now.getMonth().toString()+now.getDate().toString()+now.getHours().toString()+now.getMinutes().toString()+now.getSeconds().toString();
  var page = "json/" + data_item + ".json?" + number;
  var runtime = performance.now();
  $.getJSON(page, function(data_all){
    var id_head = data_item + "_head";
    var id_time = data_item + "_time";
    var id_content = data_item + "_content";
    var id_title = data_item + "_title";
	if(data_item == 'baidu_now' || data_item == 'baidu_today' || data_item == 'baidu_week' || data_item == 'tieba'){
		var id_head = "baidu_head";
		var id_time = "baidu_time";
		var id_content = "baidu_content";
	}
	if(data_item == 'zhihu_good' || data_item == 'zhihu_hot' || data_item == 'zhihu_daily'){
		var id_head = "zhihu_head";
		var id_time = "zhihu_time";
		var id_content = "zhihu_content";
	}
	if(data_item == 'hacpai_play' || data_item == 'hacpai_hot'){
		var id_head = "hacpai_head";
		var id_time = "hacpai_time";
		var id_content = "hacpai_content";
	}
	if(data_item == 'weixin_hot'){
		var id_head = "weixin_head";
		var id_time = "weixin_time";
		var id_content = "weixin_content";
	}
	if(data_item == 'smzdm_article_today' || data_item == 'smzdm_article_week' || data_item == 'smzdm_article_month'){
		var id_head = "smzdm_article_head";
		var id_time = "smzdm_article_time";
		var id_content = "smzdm_article_content";
	}
	if(data_item == 'itunes_paid_cn' || data_item == 'itunes_free_cn' || data_item == 'itunes_revenue_cn'){
		var id_head = "itunes_cn_head";
		var id_time = "itunes_cn_time";
		var id_content = "itunes_cn_content";
	}
	if(data_item == 'itunes_paid_us' || data_item == 'itunes_free_us' || data_item == 'itunes_revenue_us'){
		var id_head = "itunes_us_head";
		var id_time = "itunes_us_time";
		var id_content = "itunes_us_content";
	}
	if(data_item == 'toutiao_a' || data_item == 'toutiao_b' || data_item == 'toutiao_c' || data_item == 'toutiao_d' || data_item == 'toutiao_e' || data_item == 'toutiao_f' || data_item == 'toutiao_g' || data_item == 'toutiao_h' || data_item == 'toutiao_i' || data_item == 'toutiao_j'){
		var id_head = "toutiao_head";
		var id_time = "toutiao_time";
		var id_content = "toutiao_content";
	}
	if(document.getElementById(id_title)){
		if(document.getElementById("baidu_now_title")){
			if(data_item == 'baidu_today' || data_item == 'baidu_week' || data_item == 'tieba'){
				document.getElementById("baidu_now_title").style.color ='#bdbdbd';
				document.getElementById("baidu_num").style.display ='none';
			}
		}
		if(document.getElementById("baidu_today_title")){
			if(data_item == 'baidu_now' || data_item == 'baidu_week' || data_item == 'tieba'){
				document.getElementById("baidu_today_title").style.color ='#bdbdbd';
				document.getElementById("baidu_num").style.display ='none';
			}
		}
		if(document.getElementById("baidu_week_title")){
			if(data_item == 'baidu_today' || data_item == 'baidu_now' || data_item == 'tieba'){
				document.getElementById("baidu_week_title").style.color ='#bdbdbd';
				document.getElementById("baidu_num").style.display ='none';
			}
		}
		if(document.getElementById("tieba_title")){
			if(data_item == 'baidu_today' || data_item == 'baidu_now' || data_item == 'baidu_week'){
				document.getElementById("tieba_title").style.color ='#bdbdbd';
				document.getElementById("baidu_num").style.display ='inline';
			}
		}
		if(document.getElementById("zhihu_good_title")){
			if(data_item == 'zhihu_hot' || data_item == 'zhihu_daily'){
				document.getElementById("zhihu_good_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("zhihu_hot_title")){
			if(data_item == 'zhihu_good' || data_item == 'zhihu_daily'){
				document.getElementById("zhihu_hot_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("zhihu_daily_title")){
			if(data_item == 'zhihu_hot' || data_item == 'zhihu_good'){
				document.getElementById("zhihu_daily_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("hacpai_play_title")){
			if(data_item == 'hacpai_hot'){
				document.getElementById("hacpai_play_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("hacpai_hot_title")){
			if(data_item == 'hacpai_play'){
				document.getElementById("hacpai_hot_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("weixin_title")){
			if(data_item == 'weixin_hot'){
				document.getElementById("weixin_title").style.color ='#bdbdbd';
				document.getElementById("weixin_num").style.display ='none';
			}
		}
		if(document.getElementById("weixin_hot_title")){
			if(data_item == 'weixin'){
				document.getElementById("weixin_hot_title").style.color ='#bdbdbd';
				document.getElementById("weixin_num").style.display ='inline';
			}
		}
		if(document.getElementById("smzdm_article_today_title")){
			if(data_item == 'smzdm_article_week' || data_item == 'smzdm_article_month'){
				document.getElementById("smzdm_article_today_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("smzdm_article_week_title")){
			if(data_item == 'smzdm_article_today' || data_item == 'smzdm_article_month'){
				document.getElementById("smzdm_article_week_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("smzdm_article_month_title")){
			if(data_item == 'smzdm_article_today' || data_item == 'smzdm_article_week'){
				document.getElementById("smzdm_article_month_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("itunes_paid_cn_title")){
			if(data_item == 'itunes_free_cn' || data_item == 'itunes_revenue_cn'){
				document.getElementById("itunes_paid_cn_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("itunes_free_cn_title")){
			if(data_item == 'itunes_paid_cn' || data_item == 'itunes_revenue_cn'){
				document.getElementById("itunes_free_cn_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("itunes_revenue_cn_title")){
			if(data_item == 'itunes_paid_cn' || data_item == 'itunes_free_cn'){
				document.getElementById("itunes_revenue_cn_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("itunes_paid_us_title")){
			if(data_item == 'itunes_free_us' || data_item == 'itunes_revenue_us'){
				document.getElementById("itunes_paid_us_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("itunes_free_us_title")){
			if(data_item == 'itunes_paid_us' || data_item == 'itunes_revenue_us'){
				document.getElementById("itunes_free_us_title").style.color ='#bdbdbd';
			}
		}
		if(document.getElementById("itunes_revenue_us_title")){
			if(data_item == 'itunes_paid_us' || data_item == 'itunes_free_us'){
				document.getElementById("itunes_revenue_us_title").style.color ='#bdbdbd';
			}
		}
		document.getElementById(id_title).style.color ='#363636';
	}
    if(data_item != 'toutiao_b' && data_item != 'toutiao_c' && data_item != 'toutiao_d' && data_item != 'toutiao_e' && data_item != 'toutiao_f' && data_item != 'toutiao_g' && data_item != 'toutiao_h' && data_item != 'toutiao_i' && data_item != 'toutiao_j'){
      if(document.getElementById(id_head).getElementsByTagName('p')){
        document.getElementById(id_head).getElementsByTagName('p')[0].getElementsByTagName('a')[0].onclick = function(){javascript:refresh(data_item);};
      }
      if(document.getElementById(id_time)){
        document.getElementById(id_time).innerHTML = data_all['time'];
        document.getElementById(id_time).onclick = function(){javascript:refresh(data_item);};
      }
      if(document.getElementById(id_content)){
        document.getElementById(id_content).innerHTML = "";
		if(!data_all['data'][0]){
		  var tag = "<p>源站访问失败（宕机或限制）</p>";
		  document.getElementById(id_content).insertAdjacentHTML("beforeEnd",tag);
		  }
      }
    }
    for(var i = 0; i < 100; i++)
    {
      if(id_content == 'toutiao_content' && i <2){ //过滤头条前两条新闻
        continue;
      }
	  if(document.getElementById(id_content)&&data_all['data'][i]){
        var data_num = data_all['data'][i]['num'];
        var data_description = data_all['data'][i]['description'];
        var data_name = data_all['data'][i]['name'];
        var data_url = data_all['data'][i]['url'];
		if(data_description){
			atag = "\" target=\"_blank\" title=\"" + data_description + "\">"
		}else{
			atag = "\" target=\"_blank\">"
		}
        if(data_num >= 10000){
          var data_num = Math.round(data_num / 10000) + "万"
          var tag = "<li><a style=\"color:#3273dc;\" href=\"" + data_url + atag + data_name + "</a><span style=\"display:block;float:right;\">" + data_num + "</span></li>";
          document.getElementById(id_content).insertAdjacentHTML("beforeEnd",tag);
        }else if(data_num){
          var tag = "<li><a style=\"color:#3273dc;\" href=\"" + data_url + atag + data_name + "</a><span style=\"display:block;float:right;\">" + data_num + "</span></li>";
          document.getElementById(id_content).insertAdjacentHTML("beforeEnd",tag);
        }else{
          var tag = "<li><a style=\"color:#3273dc;\" href=\"" + data_url + atag + data_name + "</a></li>";
          document.getElementById(id_content).insertAdjacentHTML("beforeEnd",tag);
        }
	  }
    }
    console.log("（" + data_all['title'] + "）加载完成", "耗时:" + (performance.now() - runtime).toFixed(2) + "ms", "总耗时:" + performance.now().toFixed(2) + "ms");
  }
  )
};

html_xr('baidu_now');
html_xr('weibo');
html_xr('weixin');
html_xr('v2ex');
html_xr('jandan');
html_xr('zhihu_good');
html_xr('hostloc');
html_xr('smzdm_article_today');
html_xr('douban');
html_xr('hacpai_play');
html_xr('guokr');
html_xr('chouti');
html_xr('cnbeta');
html_xr('mop');
html_xr('solidot');
html_xr('cctv');
html_xr('toutiao_a');
html_xr('tianya');
html_xr('ithome');
html_xr('zaobao');
html_xr('thepaper');
html_xr('huxiu');
html_xr('nytimes');
html_xr('bjnews');
html_xr('sinatech');
html_xr('itunes_free_cn');
html_xr('itunes_free_us');
setTimeout("html_xr('toutiao_b')",1000);
setTimeout("html_xr('toutiao_c')",1000);
setTimeout("html_xr('toutiao_d')",1000);
setTimeout("html_xr('toutiao_e')",1000);
setTimeout("html_xr('toutiao_f')",1000);
setTimeout("html_xr('toutiao_g')",1000);
setTimeout("html_xr('toutiao_h')",1000);
setTimeout("html_xr('toutiao_i')",1000);
setTimeout("html_xr('toutiao_j')",1000);
