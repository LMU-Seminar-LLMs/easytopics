import { useState, useEffect, React } from 'react';
import MainHeadline from '../../components/typography/MainHeadline';
import DefaultParagraph from '../../components/typography/DefaultParagraph';
import DataTable from '../../components/DataTable';
import { Button, TextField } from '@mui/material';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { CircularProgress } from '@mui/material';

import {
  DataGrid,
  GridColDef,
  GridFilterModel,
  GridFilterItem,
} from '@mui/x-data-grid';

interface Question {
  id: number;
  question: string;
}

const columns: GridColDef[] = [
  {
    field: 'id',
    headerName: 'ID',
    type: 'number',
    flex: 1,
    headerAlign: 'center',
    align: 'center',
    headerClassName: '',
  },
  {
    field: 'doc',
    headerName: 'Text',
    type: 'text',
    flex: 4,
    headerClassName: '',
  },
  {
    field: 'question',
    headerName: 'Question',
    type: 'text',
    flex: 2,
    headerClassName: '',
  },
  {
    field: 'answer',
    headerName: 'Answer',
    type: 'text',
    flex: 4,
    headerClassName: '',
  },
];

const Qa: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [tableData, setTableData] = useState<any[] | null>(null);
  const [triedQuestions, setTriedQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const fetchQuestions = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/questions');
      const data = await response.json();

      if (response.ok) {
        setTriedQuestions(data);
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchAnswers = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`http://localhost:5000/answers`);
      const data = await response.json();

      if (response.ok) {
        setTableData(data);
      } else {
        setTableData(null);
      }
    } catch (error) {
      console.error('Error fetching answers:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteQuestion = async (questionId: number) => {
    try {
      const response = await fetch(
        `http://localhost:5000/questions/${questionId}`,
        {
          method: 'DELETE',
        }
      );

      if (response.ok) {
        console.log(`Question with id ${questionId} deleted.`);
      }
    } catch (error) {
      console.error('Error deleting question:', error);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    fetchQuestions();
    fetchAnswers();
    setIsLoading(false);
  }, []);

  const handleTryOn5Click = async () => {
    if (inputValue) {
      try {
        setIsLoading(true);
        // ask the question
        const response = await fetch('http://localhost:5000/ask_question', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: inputValue, tryout: true, k: 5 }),
        });

        if (response.ok) {
          fetchQuestions();
          fetchAnswers();
        }
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleDeleteQuestion = async (questionId: number) => {
    await deleteQuestion(questionId);
    setTriedQuestions((prevQuestions) =>
      prevQuestions.filter((question) => question.id !== questionId)
    );
    fetchAnswers();
  };

  const handleAskToAllClick = async () => {
    try {
      setIsLoading(true);
      // ask the question
      const response = await fetch('http://localhost:5000/ask_question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tryout: false }),
      });

      if (response.ok) {
        fetchQuestions();
        fetchAnswers();
        console.log('API call for Ask to all documents with:');
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className='container mx-auto p-4'>
        <MainHeadline text='Ask a question' />
        <DefaultParagraph text='In the text field below enter a question that will be asked to each text. First, ask your question on 5 documents to get a sense of how well the question works. Afterwards you can ask another question or directly ask it on all documents.' />
        <DefaultParagraph text='Ask relevant open-ended questions, refrain from asking questions with "one word answers".' />
        <div className='pt-8'>
          <TextField
            label='Enter your question'
            variant='outlined'
            fullWidth
            value={inputValue}
            onChange={handleInputChange}
          />
        </div>
        <div className='mt-2'>
          <>
            <Button onClick={handleTryOn5Click} disabled={!inputValue}>
              Try on 5 documents
            </Button>
            <Button onClick={() => setInputValue('')} disabled={!inputValue}>
              Add another question
            </Button>
            <Button
              onClick={handleAskToAllClick}
              disabled={triedQuestions.length == 0}
            >
              'Ask Question(s) to all documents'
            </Button>
          </>
        </div>
        <div className='mt-2'>
          <DefaultParagraph text='You can ask multiple questions to the same document. The questions will be saved in the database.' />
        </div>
        <div className='mt-2'>
          {triedQuestions.length > 0 ? (
            <ul className='pl-4'>
              {triedQuestions.map((question) => (
                <li key={question.id}>
                  <XMarkIcon
                    className='h-4 w-4 inline-block text-red-500'
                    onClick={(event) => {
                      event.stopPropagation();
                      handleDeleteQuestion(question.id);
                    }}
                  />
                  <span className='pr-2'>({question.id})</span>
                  <span className='pr-2'>{question.question}</span>
                </li>
              ))}
            </ul>
          ) : (
            <div className='italic text-gray-500 font-light p-2'>
              -- No questions have been tried yet. --
            </div>
          )}
        </div>
        <div className='container mx-auto'>
          <MainHeadline text='Preview' />
          {tableData && tableData.length > 0 ? (
            <>
              <div className='italic text-gray-500 pb-2'>
                <DefaultParagraph text='Hover over column names for sort and filter options.' />
              </div>
              {isLoading ? (
                <div className='flex justify-center pt-5'>
                  <div className='loading-container'>
                    <CircularProgress />
                  </div>
                </div>
              ) : (
                <DataTable columns={columns} data={tableData} />
              )}
            </>
          ) : (
            <div className='italic text-gray-500 font-light p-2'>
              -- You need to first ask a question to see the answers... --
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Qa;
