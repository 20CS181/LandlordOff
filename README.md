# Landlord Off
This project is the final for the CS181: Artificial Intelligence @Shanghaitech, **completely from scratch**.   

Landlord Off, or Dou Di Zhu, is a popular card game in China, especially during the Chinese Lunar New Year. We implemented the card game interactions with three computer agents, including a random agent and two AI agent, and one human agent, through which one could play with a computer agent or a human as well. The improved AI agent turned out to achieve an outcome of 18% rise in the winning rate.
You could access our Documents [here](https://github.com/20CS181/LandlordOffDcuments), containing a final report and presentation slides.

The code structure referred to our homework, the Pacman Games borrowed from the [CS188 course at UC Berkeley](https://inst.eecs.berkeley.edu/~cs188/sp21/). It turned out so simple and elegant with OOP game developing with Python and we love it!

## References:
As a start, we read docs linked below for refrences, but didn't copy any. The final version borrows some scoring strategies from an old Chinese card book.

- [简书 - 斗地主策略](https://www.jianshu.com/p/9fb001daedcf)
- [洛谷 - 猪国杀](https://www.luogu.com.cn/problem/P2482)
- [blog](https://ninesun.blog.csdn.net/article/list/3)

## Plan before 1st pre
1. Pokers delivery in random.
2. Legal potions.
3. Winner judgement.


## Agents
(last updated: 12/12, 2020)
### in `HumanAgent.py`:
claim `class Agent`, `class HumanAgent`.
(`utils.py`, `play.py`用来测试`HumanAgent`)

### in `AIagent.py`:
A normal AI_agent randomly puts cards

## Game playing
### in `main.py`:
the main process to play game.

### in `game.py`:
some necessary class and function of the GameState

## Play the Game
* To play the game, run `main.py`.
* For the rules, there are 10 legal card types:('a''b' in range(3, 10), 'x''X' are two kings, no joker)
1. dan_pai:         ['a']
2. two same:        ['a','a']
3. three same       ['a','a','a']
4. three_plus_one   ['a','a','a','b']
5. three_plus_two   ['a','a','a','b','b']
6. dan_lian         ['a','b','c']
7. er_lian          ['a','a','b','b']
8. san_lian         ['a','a','a','b','b','b']
9. bomb:            ['a','a','a','a']
10. king bomb:      ['x','X']
* 6\7\8 are `shun_zi`, which we don't have a strict constraint, so please be nice to ai.
