'use client'

import { useEffect, useRef, useState } from 'react'

export default function HomePage() {
  const slides = [1, 2, 3, 4, 5]
  const [currentIndex, setCurrentIndex] = useState(0)
  const timeoutRef = useRef<NodeJS.Timeout | null>(null)
  const carouselRef = useRef<HTMLDivElement>(null)

  const resetTimeout = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current)
  }

  useEffect(() => {
    const startAutoSlide = () => {
      timeoutRef.current = setTimeout(() => {
        setCurrentIndex((prevIndex) =>
          prevIndex === slides.length - 1 ? 0 : prevIndex + 1
        )
      }, 2000)
    }

    startAutoSlide()

    return () => {
      resetTimeout()
    }
  }, [currentIndex])

  const handleMouseEnter = () => {
    resetTimeout()
  }

  const handleMouseLeave = () => {
    timeoutRef.current = setTimeout(() => {
      setCurrentIndex((prevIndex) =>
        prevIndex === slides.length - 1 ? 0 : prevIndex + 1
      )
    }, 2000)
  }

  return (
    <div className="min-h-screen w-full bg-gray-50">
      {/* Carousel Container */}
      <section className="max-w-7xl mx-auto px-4 py-10">
        <div
          ref={carouselRef}
          className="bg-white rounded-2xl shadow-lg overflow-hidden relative cursor-pointer"
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          {/* Slider wrapper */}
          <div
            className="flex transition-transform duration-500 ease-in-out"
            style={{
              transform: `translateX(-${currentIndex * 100}%)`,
              width: `${slides.length * 100}%`,
            }}
          >
            {slides.map((item) => (
              <div
                key={item}
                className="w-full flex-shrink-0 flex items-center justify-center h-140 bg-blue-100 text-blue-800 text-2xl font-semibold"
                style={{ width: `${100 / slides.length}%` }}
              >
                Slide {item}
              </div>
            ))}
          </div>

          {/* Dots */}
          <div className="flex justify-center gap-2 py-3 bg-white border-t border-gray-100">
            {slides.map((_, idx) => (
              <button
                key={idx}
                className={`h-3 w-3 rounded-full transition-colors ${
                  currentIndex === idx ? 'bg-blue-600' : 'bg-gray-300'
                }`}
                onClick={() => setCurrentIndex(idx)}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Paragraph */}
      <section className="max-w-7xl mx-auto px-4 pb-20">
        <h2 className="text-3xl font-bold mb-4">Welcome to the Admissions Portal</h2>
        <p className="text-gray-700 leading-7">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce euismod,
          turpis et dapibus suscipit, ligula lorem malesuada arcu, sed gravida
          velit justo nec eros. Integer facilisis, velit ac sodales fringilla,
          turpis lorem dapibus nulla, sed fermentum nunc sapien vel magna. Morbi
          lobortis suscipit lorem, nec faucibus neque consequat ac. Aenean vel
          rhoncus mauris. Sed vitae convallis turpis. Pellentesque nec tortor
          sapien. Mauris et placerat magna. In id neque quis nisl dignissim
          interdum non nec lacus. Sed aliquam dapibus eros, nec elementum felis
          posuere eget. Nullam fermentum dolor vel leo rhoncus fermentum. Proin
          lacinia nibh nec tincidunt volutpat.
        </p>
      </section>
    </div>
  )
}
