/**
 * 随机昵称常量
 *
 * 用于匿名用户自动生成昵称
 */

export const RANDOM_NICKNAMES = [
  '好奇的猫咪', '爱思考的云朵', '路过的旅人', '安静的观察者',
  '快乐的星星', '温柔的微风', '勇敢的小鸟', '智慧的树洞',
  '神秘的访客', '温暖的阳光', '自由的飞鸟', '善良的小熊',
  '可爱的兔子', '机智的狐狸', '优雅的天鹅', '活泼的松鼠',
  '沉稳的大象', '灵动的蝴蝶', '坚定的山峰', '清澈的溪流'
] as const

export type RandomNickname = typeof RANDOM_NICKNAMES[number]

/**
 * 生成随机昵称
 * 从预设列表中随机选择一个，并加上随机数字后缀
 */
export const generateNickname = (): string => {
  const randomIndex = Math.floor(Math.random() * RANDOM_NICKNAMES.length)
  const randomNum = Math.floor(Math.random() * 1000)
  return `${RANDOM_NICKNAMES[randomIndex]}${randomNum}`
}
