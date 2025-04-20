import Card from "@/components/card/Card"

const AboutPage = () => {
  return (
    <div className=' text-white'>

        <section className='min-h-[50vh] bg-pattern flex flex-col justify-center items-center'>
            <h1 className='font-bold text-5xl m-6'>SpeedSolver</h1>
            <p>Cистема эффективного управления</p>
        </section>

        <section className='p-6 bg-black min-h-[50vh]'>
        
            <div>
                <div className="flex flex-col gap-6">
                <h1 className='font-bold text-3xl'>Мы используем</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <Card>
                    <h2 className="text-2xl font-bold">Backend</h2>
                    <ul>
                        <li>Python</li>
                        <li>FastAPI</li>
                        <li>Pydantic</li>
                        <li>Uvicorn</li>
                    </ul>
                </Card>
                <Card>
                    <h2 className="text-2xl font-bold">Frontend</h2>
                    <ul>
                        <li>React</li>
                        <li>Typescript</li>
                        <li>Tailwind</li>
                    </ul>
                </Card>

                <div className="flex flex-col gap-6">
                    <Card>
                        <h2 className="text-2xl font-bold">ORM</h2>
                        <ul>
                            <li>Python SQLAlchemy</li>
                            <li>Alembic</li>
                            <li>asyncpg driver</li>
                        </ul>
                    </Card>
                    <Card>
                        <h2 className="text-2xl font-bold">Мониторинг</h2>
                        <ul>
                            <li>Grafana</li>
                            <li>Prometheus</li>
                            <li>Node Exporter</li>
                            <li>AlertManager</li>
                        </ul>
                    </Card>

                </div>
                <div className="grid grid-cols-1 lg:grid-cols-auto lg: grid-rows-2 gap-6">
                    <Card><p>База денных: PostgreSQL</p></Card>
                    <Card><p>Авторизация: JWT / pyjwt</p></Card>
                    <Card><p>Тестирование: pytest</p></Card>
                </div>
                    
                <div className="grid grid-cols-1 lg:grid-cols-auto lg: grid-rows-2 gap-6">
                    <Card><p>Контейнеризация: Docker</p></Card>
                    <Card><p>Веб-сервер: Nginx</p></Card>
                    <Card><p>CI / CD: Github Actions</p></Card>
                </div>

                
            </div>
            </div>
            </div>

        </section>
        
    </div>
  )
}

export default AboutPage