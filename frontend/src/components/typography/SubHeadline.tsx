type SubHeadlineProps = {
  text: string;
};

const SubHeadline = ({ text }: SubHeadlineProps) => (
  <h2 className='font-bold text-xl/loose'>{text}</h2>
);

export default SubHeadline;
