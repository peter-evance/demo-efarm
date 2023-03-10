import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DairyCowUpdateComponent } from './dairy-cow-update.component';

describe('DairyCowUpdateComponent', () => {
  let component: DairyCowUpdateComponent;
  let fixture: ComponentFixture<DairyCowUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DairyCowUpdateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DairyCowUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
