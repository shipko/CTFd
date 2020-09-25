import CTFd from "../CTFd";
import $ from "jquery";
import Moment from "moment";
import nunjucks from "nunjucks";
import { Howl } from "howler";
import events from "../events";
import config from "../config";
import styles from "../styles";
import times from "../times";
import { default as helpers } from "../helpers";
import { ezAlert } from "../ezq";


CTFd.init(window.init);
window.CTFd = CTFd;
window.helpers = helpers;
window.$ = $;
window.Moment = Moment;
window.nunjucks = nunjucks;
window.Howl = Howl;

$(() => {
  styles();
  times();
  events(config.urlRoot);
});


if (!window.localStorage.getItem('starMirWelcome')) {
    ezAlert({
        title: "Да пребудет с тобой сила!",
        body: '<p><img src="https://sun9-39.userapi.com/c851120/v851120018/187550/ukLQzp_WWlo.jpg" style="margin-right: 20px; max-width: 400px; float: left;">Добро пожаловать в центр обучения!</p>\n' +
            '<p>Здесь ты постигнешь секреты Вселенной по безопасной разработке ПО. Ты готов пройти путь от падавана до джедая? Путь этот будет не прост, однако и награда ожидает тебя приятная. Покажешь себя хорошо - попадешь в галактическую команду безопасности</p>',
        button: "Начинаем!",
        large: true
    });
}