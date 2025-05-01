import Card from "@/components/card/Card"
import { useBreakpoint } from "@/hooks/use-breackpoint"
import { useState } from "react"

const AboutPage = () => {
  const isTablet = useBreakpoint(1024)
  const isMobile = useBreakpoint(786)
  const [showAll, setShowAll] = useState(false)

  const toggleShowAll = () => setShowAll(!showAll)

  const visibleBlocksCount = !isTablet ? 3 : isMobile ? 1 : 2 // 0-based index: блоков по 2 карточки (первая строка = блок 0, ORM+Мониторинг = блок 1 и т.д.)

  const blocks = [
    (
      <div key="block0" className="flex flex-col md:flex-row gap-6 md:col-span-2 lg:col-span-1">
        <Card style="highlight">
          <h2 className="text-2xl font-bold">Backend</h2>
          <ul>
            <li>Python</li>
            <li>FastAPI</li>
            <li>Pydantic</li>
            <li>Uvicorn</li>
          </ul>
        </Card>

        <Card style="highlight">
          <h2 className="text-2xl font-bold">Frontend</h2>
          <ul>
            <li>React</li>
            <li>Typescript</li>
            <li>Tailwind</li>
          </ul>
        </Card>
      </div>
    ),
    (
      <div key="block1" className="grid grid-cols-1 md:grid-cols-2 gap-6 md:col-span-2">
        <Card style="highlight">
          <h2 className="text-2xl font-bold">ORM</h2>
          <ul>
            <li>Python SQLAlchemy</li>
            <li>Alembic</li>
            <li>asyncpg driver</li>
          </ul>
        </Card>
        <Card style="highlight">
          <h2 className="text-2xl font-bold">Мониторинг</h2>
          <ul>
            <li>Grafana</li>
            <li>Prometheus</li>
            <li>Node Exporter</li>
            <li>AlertManager</li>
          </ul>
        </Card>
      </div>
    ),
    (
      <div key="block2" className="grid grid-cols-1 lg:grid-cols-3 gap-6 col-span-1 md:col-span-2 lg:col-span-3">
        <Card style="highlight"><p>База денных: PostgreSQL</p></Card>
        <Card style="highlight"><p>Авторизация: JWT / pyjwt</p></Card>
        <Card style="highlight"><p>Тестирование: pytest</p></Card>
      </div>
    ),
    (
      <div key="block3" className="grid grid-cols-1 lg:grid-cols-3 gap-6 col-span-1 md:col-span-2 lg:col-span-3">
        <Card style="highlight"><p>Контейнеризация: Docker</p></Card>
        <Card style="highlight"><p>Веб-сервер: Nginx</p></Card>
        <Card style="highlight"><p>CI / CD: Github Actions</p></Card>
      </div>
    )
  ]

  // Логика отображения блоков
  const displayedBlocks = showAll || !isTablet ? blocks : blocks.slice(0, visibleBlocksCount)

  return (
    <div className='text-white'>
      <section className='min-h-[50vh] bg-pattern flex flex-col justify-center items-center'>
        <h1 className='font-bold text-5xl m-6'>SpeedSolver</h1>
        <p>Cистема эффективного управления</p>
      </section>

      <section className='p-6 bg-black min-h-[50vh]'>
        <div className="flex flex-col gap-6">
          <h1 className='font-bold text-3xl'>Мы используем</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {displayedBlocks}
          </div>
          {isTablet && (
            <button
              onClick={toggleShowAll}
              className="glass-button !bg-[#2d2d2d]"
            >
              {showAll ? "Скрыть" : "Показать все"}
            </button>
          )}
        </div>
      </section>
    </div>
  )
}

export default AboutPage
