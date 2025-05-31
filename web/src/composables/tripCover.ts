import cover1 from '../assets/trip-covers/1.png'
import cover2 from '../assets/trip-covers/2.png'
import cover3 from '../assets/trip-covers/3.png'
import cover4 from '../assets/trip-covers/4.png'
import cover5 from '../assets/trip-covers/5.png'
import cover6 from '../assets/trip-covers/6.png'
import cover7 from '../assets/trip-covers/7.png'
import cover8 from '../assets/trip-covers/8.png'

export const useTripCover = (tripName: string): string => {
  const stringToNumber = (input: string): number => {
    let hash = 0
    if (input.length === 0) return hash

    for (let i = 0; i < input.length; i++) {
      const charCode = input.charCodeAt(i)
      hash = (hash << 5) - hash + charCode
      hash |= 0 // Convert to 32bit integer
    }

    // Normalize the hash to be between 1 and 8
    return Math.abs(hash % 8)
  }

  const covers = [
    cover1,
    cover2,
    cover3,
    cover4,
    cover5,
    cover6,
    cover7,
    cover8,
  ]

  return covers[stringToNumber(tripName)]
}
