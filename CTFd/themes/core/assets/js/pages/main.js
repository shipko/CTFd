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
            '<p>В галактическом сенате смятение... <br />Пока бойцы сопротивления находятся в самых разных концах Мира, всеми силами поддерживая связь и эффективность работы - вирусы, ошибки и уязвимости появляются внезапно и наносят непоправимый вред Системам. Отряду, ответственному за мировую безопасность нужна поддержка. Они готовы поделиться знаниями со всеми, но стать одним из рыцарей Ордена не так просто. Есть ли у Светлой стороны шанс оказаться сильнее? Возможно, но пока известно только одно - этот путь не будет простым.</p> ' +
            '<p>Вам предстоит пройти испытания, чтобы быть готовым встать в наши ряды, и выйти в Мир.</p>',
        button: "Начинаем!",
        xlarge: true
    });
}