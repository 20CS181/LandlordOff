# land_lord_off
For CS181 final project in Shanghaitech. The structure referred to our homework, the Pacman Games of the [CS188 at UC Berkeley](https://inst.eecs.berkeley.edu/~cs188/sp21/). It turned out so simple and elegant with OOP game developing with Python and we love it!

## References:
(We read these just for refrences, but didn't implement any)
### 简书上的斗地主策略 https://www.jianshu.com/p/9fb001daedcf
### 洛谷猪国杀 https://www.luogu.com.cn/problem/P2482
### 比较全面的相关算法 https://ninesun.blog.csdn.net/article/list/3

## Plan before 1st pre
1. Pokers delivery in random.
2. Legal potions.
3. Winner judgement.


## Agents
### in `HumanAgent.py`:
12/ 12
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
* For the rules, there are 10 legal card types:('a''b' in range(3, 10), 'x''X' are kings)
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
