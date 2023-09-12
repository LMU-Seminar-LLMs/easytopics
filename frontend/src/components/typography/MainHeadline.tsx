type MainHeadlineProps = {
  text: string;
};

const MainHeadline = ({ text }: MainHeadlineProps) => (
  <h1 className='font-bold text-4xl/loose'>{text}</h1>
);

export default MainHeadline;
